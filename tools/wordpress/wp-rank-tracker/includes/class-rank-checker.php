<?php
if (!defined('ABSPATH')) {
    exit;
}

class WPRT_Rank_Checker {

    public static function clean_domain($domain) {
        if (empty($domain)) return '';
        $d = trim(strtolower($domain));
        if (strpos($d, '://') !== false) {
            $parts = explode('://', $d);
            $d = $parts[1];
        }
        if (strpos($d, '/') !== false) {
            $parts = explode('/', $d);
            $d = $parts[0];
        }
        if (strpos($d, ':') !== false) {
            $parts = explode(':', $d);
            $d = $parts[0];
        }
        if (strpos($d, 'www.') === 0) {
            $d = substr($d, 4);
        }
        return $d;
    }

    public static function domain_matches($url, $target_domain, $wildcard = true) {
        if (empty($url) || empty($target_domain)) return false;
        $u = self::clean_domain($url);
        $t = self::clean_domain($target_domain);

        if ($wildcard) {
            return ($u === $t || (strlen($u) > strlen($t) && substr($u, -strlen('.' . $t)) === '.' . $t));
        } else {
            return ($u === $t || $u === 'www.' . $t);
        }
    }

    public static function check_rank($keyword, $domain, $gl = 'in', $hl = 'en', $api_key = '') {
        if (empty($api_key)) {
            $api_key = get_option('wprt_serper_api_key', '499a4c6f466313cc4dadb69021321bfb14547034');
        }

        if (empty($api_key)) {
            return ['error' => 'Missing Serper API Key. Please configure it in Settings.'];
        }

        $url = 'https://google.serper.dev/search';
        $payload = [
            'q'   => $keyword,
            'gl'  => strtolower($gl),
            'hl'  => strtolower($hl),
            'num' => 100
        ];

        $response = wp_remote_post($url, [
            'method'    => 'POST',
            'timeout'   => 20,
            'headers'   => [
                'X-API-KEY'    => trim($api_key),
                'Content-Type' => 'application/json'
            ],
            'body'      => json_encode($payload)
        ]);

        if (is_wp_error($response)) {
            return ['error' => $response->get_error_message()];
        }

        $status_code = wp_remote_retrieve_response_code($response);
        $body = wp_remote_retrieve_body($response);

        if ($status_code !== 200) {
            return ['error' => 'API returned code ' . $status_code . ': ' . $body];
        }

        $data = json_decode($body, true);
        if (!$data || !isset($data['organic'])) {
            return ['rank' => null, 'url' => 'Not ranked in Top 100'];
        }

        $organic = $data['organic'];
        foreach ($organic as $item) {
            $link = isset($item['link']) ? $item['link'] : '';
            if (self::domain_matches($link, $domain, true)) {
                $pos = isset($item['position']) ? intval($item['position']) : 0;
                return [
                    'rank' => $pos,
                    'url'  => $link
                ];
            }
        }

        return [
            'rank' => null,
            'url'  => 'Not ranked in Top 100'
        ];
    }
}
