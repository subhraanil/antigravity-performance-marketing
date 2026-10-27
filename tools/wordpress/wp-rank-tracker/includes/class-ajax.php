<?php
if (!defined('ABSPATH')) {
    exit;
}

class WPRT_Ajax {

    public static function init() {
        add_action('wp_ajax_wprt_check_single_rank', [__CLASS__, 'check_single_rank']);
        add_action('wp_ajax_wprt_delete_keyword', [__CLASS__, 'delete_keyword']);
        add_action('admin_post_wprt_export_csv', [__CLASS__, 'export_csv']);
        add_action('wp_ajax_wprt_frontend_check', [__CLASS__, 'frontend_check']);
        add_action('wp_ajax_nopriv_wprt_frontend_check', [__CLASS__, 'frontend_check']);
    }

    public static function check_single_rank() {
        check_ajax_referer('wprt_nonce', 'nonce');

        if (!current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }

        $keyword_id = isset($_POST['keyword_id']) ? intval($_POST['keyword_id']) : 0;
        if (!$keyword_id) {
            wp_send_json_error('Invalid keyword ID');
        }

        $kw_data = WPRT_DB::get_keyword($keyword_id);
        if (!$kw_data) {
            wp_send_json_error('Keyword not found');
        }

        $target_domain = get_option('wprt_target_domain', '');
        if (empty($target_domain)) {
            $target_domain = home_url();
        }

        $gl = get_option('wprt_target_region', 'in');
        $hl = get_option('wprt_target_language', 'en');
        $api_key = get_option('wprt_serper_api_key', '499a4c6f466313cc4dadb69021321bfb14547034');

        $result = WPRT_Rank_Checker::check_rank($kw_data->keyword, $target_domain, $gl, $hl, $api_key);

        if (isset($result['error'])) {
            wp_send_json_error($result['error']);
        }

        $rank = $result['rank'];
        $url = $result['url'];

        WPRT_DB::update_rank($keyword_id, $rank, $url);

        $updated_kw = WPRT_DB::get_keyword($keyword_id);

        wp_send_json_success([
            'id'            => $keyword_id,
            'current_rank'  => $updated_kw->current_rank,
            'previous_rank' => $updated_kw->previous_rank,
            'ranked_url'    => $updated_kw->ranked_url,
            'last_checked'  => $updated_kw->last_checked
        ]);
    }

    public static function delete_keyword() {
        check_ajax_referer('wprt_nonce', 'nonce');

        if (!current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }

        $keyword_id = isset($_POST['keyword_id']) ? intval($_POST['keyword_id']) : 0;
        if (!$keyword_id) {
            wp_send_json_error('Invalid keyword ID');
        }

        WPRT_DB::delete_keyword($keyword_id);
        wp_send_json_success('Deleted');
    }

    public static function export_csv() {
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }

        $keywords = WPRT_DB::get_all_keywords();

        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename=google_keyword_rankings_' . date('Y-m-d') . '.csv');

        $output = fopen('php://output', 'w');
        fputcsv($output, ['#', 'Keyword', 'Current Rank', 'Previous Rank', 'Ranked Landing Page URL', 'Last Checked Date']);

        $i = 1;
        foreach ($keywords as $kw) {
            $rank_display = ($kw->current_rank !== null && $kw->current_rank > 0) ? $kw->current_rank : 'Not ranked';
            $prev_display = ($kw->previous_rank !== null && $kw->previous_rank > 0) ? $kw->previous_rank : '-';
            
            fputcsv($output, [
                $i++,
                $kw->keyword,
                $rank_display,
                $prev_display,
                $kw->ranked_url,
                $kw->last_checked
            ]);
        }
        fclose($output);
        exit;
    }

    public static function frontend_check() {
        check_ajax_referer('wprt_frontend_nonce', 'nonce');

        $keyword = isset($_POST['keyword']) ? sanitize_text_field(trim($_POST['keyword'])) : '';
        $domain  = isset($_POST['domain']) ? sanitize_text_field(trim($_POST['domain'])) : '';
        $region  = isset($_POST['region']) ? sanitize_text_field(trim($_POST['region'])) : 'in';

        if (empty($keyword) || empty($domain)) {
            wp_send_json_error('Missing keyword or domain');
        }

        $hl = get_option('wprt_target_language', 'en');
        $api_key = get_option('wprt_serper_api_key', '499a4c6f466313cc4dadb69021321bfb14547034');

        $result = WPRT_Rank_Checker::check_rank($keyword, $domain, $region, $hl, $api_key);

        if (isset($result['error'])) {
            wp_send_json_error($result['error']);
        }

        wp_send_json_success([
            'rank' => $result['rank'],
            'url'  => $result['url']
        ]);
    }
}
