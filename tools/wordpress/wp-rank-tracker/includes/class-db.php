<?php
if (!defined('ABSPATH')) {
    exit;
}

class WPRT_DB {

    public static function create_tables() {
        global $wpdb;
        $charset_collate = $wpdb->get_charset_collate();

        $table_keywords = $wpdb->prefix . 'wprt_keywords';
        $table_history  = $wpdb->prefix . 'wprt_history';

        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');

        $sql_keywords = "CREATE TABLE IF NOT EXISTS $table_keywords (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            keyword VARCHAR(255) NOT NULL,
            current_rank INT(11) DEFAULT NULL,
            previous_rank INT(11) DEFAULT NULL,
            ranked_url TEXT DEFAULT NULL,
            last_checked DATETIME DEFAULT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY  (id),
            UNIQUE KEY keyword (keyword)
        ) $charset_collate;";

        $sql_history = "CREATE TABLE IF NOT EXISTS $table_history (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
            keyword_id BIGINT(20) UNSIGNED NOT NULL,
            rank_val INT(11) DEFAULT NULL,
            ranked_url TEXT DEFAULT NULL,
            checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY  (id),
            KEY keyword_id (keyword_id)
        ) $charset_collate;";

        dbDelta($sql_keywords);
        dbDelta($sql_history);
    }

    public static function add_keywords($keywords_raw) {
        global $wpdb;
        $table_keywords = $wpdb->prefix . 'wprt_keywords';
        
        $lines = preg_split('/[\r\n,]+/', $keywords_raw);
        $added = 0;

        foreach ($lines as $line) {
            $kw = trim($line);
            if (!empty($kw)) {
                $inserted = $wpdb->insert(
                    $table_keywords,
                    [
                        'keyword' => sanitize_text_field($kw),
                        'created_at' => current_time('mysql')
                    ],
                    ['%s', '%s']
                );
                if ($inserted) {
                    $added++;
                }
            }
        }
        return $added;
    }

    public static function get_all_keywords() {
        global $wpdb;
        $table = $wpdb->prefix . 'wprt_keywords';
        return $wpdb->get_results("SELECT * FROM $table ORDER BY id ASC");
    }

    public static function get_keyword($id) {
        global $wpdb;
        $table = $wpdb->prefix . 'wprt_keywords';
        return $wpdb->get_row($wpdb->prepare("SELECT * FROM $table WHERE id = %d", $id));
    }

    public static function update_rank($keyword_id, $new_rank, $ranked_url) {
        global $wpdb;
        $table_keywords = $wpdb->prefix . 'wprt_keywords';
        $table_history  = $wpdb->prefix . 'wprt_history';

        $current = $wpdb->get_row($wpdb->prepare("SELECT current_rank FROM $table_keywords WHERE id = %d", $keyword_id));
        $prev_rank = ($current && isset($current->current_rank)) ? $current->current_rank : null;

        $wpdb->update(
            $table_keywords,
            [
                'previous_rank' => $prev_rank,
                'current_rank'  => $new_rank,
                'ranked_url'    => $ranked_url,
                'last_checked'  => current_time('mysql')
            ],
            ['id' => $keyword_id],
            ['%d', '%d', '%s', '%s'],
            ['%d']
        );

        $wpdb->insert(
            $table_history,
            [
                'keyword_id' => $keyword_id,
                'rank_val'   => $new_rank,
                'ranked_url' => $ranked_url,
                'checked_at' => current_time('mysql')
            ],
            ['%d', '%d', '%s', '%s']
        );
    }

    public static function delete_keyword($id) {
        global $wpdb;
        $table_keywords = $wpdb->prefix . 'wprt_keywords';
        $table_history  = $wpdb->prefix . 'wprt_history';

        $wpdb->delete($table_history, ['keyword_id' => $id], ['%d']);
        return $wpdb->delete($table_keywords, ['id' => $id], ['%d']);
    }
}
