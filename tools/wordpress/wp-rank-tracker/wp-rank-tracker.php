<?php
/**
 * Plugin Name: Unrestricted Google Keyword Rank Tracker
 * Plugin URI: https://github.com/indranilbanerjee/digital-marketing-pro
 * Description: An unrestricted, domain-lock-free Google SERP keyword rank checker for WordPress. Powered by high-speed Serper.dev API.
 * Version: 1.0.0
 * Author: Antigravity Performance Marketing OS
 * Text Domain: wp-rank-tracker
 */

if (!defined('ABSPATH')) {
    exit;
}

define('WPRT_VERSION', '1.0.0');
define('WPRT_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('WPRT_PLUGIN_URL', plugin_dir_url(__FILE__));

require_once WPRT_PLUGIN_DIR . 'includes/class-db.php';
require_once WPRT_PLUGIN_DIR . 'includes/class-rank-checker.php';
require_once WPRT_PLUGIN_DIR . 'includes/class-ajax.php';
require_once WPRT_PLUGIN_DIR . 'includes/class-frontend.php';

// Activation Hook
register_activation_hook(__FILE__, function() {
    WPRT_DB::create_tables();
    if (!get_option('wprt_serper_api_key')) {
        update_option('wprt_serper_api_key', '499a4c6f466313cc4dadb69021321bfb14547034');
    }
    if (get_option('wprt_target_domain') === false) {
        update_option('wprt_target_domain', '');
    }
    if (!get_option('wprt_target_region')) {
        update_option('wprt_target_region', 'in');
    }
    if (!get_option('wprt_target_language')) {
        update_option('wprt_target_language', 'en');
    }
});

// Initialize AJAX & Frontend Shortcodes
WPRT_Ajax::init();
WPRT_Frontend::init();

// Admin Menu
add_action('admin_menu', function() {
    add_menu_page(
        'Rank Tracker',
        'Rank Tracker',
        'manage_options',
        'wp-rank-tracker',
        'wprt_render_dashboard_page',
        'dashicons-chart-line',
        30
    );

    add_submenu_page(
        'wp-rank-tracker',
        'All Keywords',
        'All Keywords',
        'manage_options',
        'wp-rank-tracker',
        'wprt_render_dashboard_page'
    );

    add_submenu_page(
        'wp-rank-tracker',
        'Settings',
        'Settings',
        'manage_options',
        'wp-rank-tracker-settings',
        'wprt_render_settings_page'
    );
});

// Enqueue Scripts and Styles
add_action('admin_enqueue_scripts', function($hook) {
    if (strpos($hook, 'wp-rank-tracker') === false) {
        return;
    }

    wp_enqueue_style('wprt-admin-css', WPRT_PLUGIN_URL . 'assets/css/admin.css', [], WPRT_VERSION);
    wp_enqueue_script('wprt-admin-js', WPRT_PLUGIN_URL . 'assets/js/admin.js', ['jquery'], WPRT_VERSION, true);

    wp_localize_script('wprt-admin-js', 'wprtData', [
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce'    => wp_create_nonce('wprt_nonce')
    ]);
});

// Handle Form Submissions (Add Keywords)
add_action('admin_init', function() {
    if (isset($_POST['wprt_action']) && $_POST['wprt_action'] === 'add_keywords') {
        check_admin_referer('wprt_add_keywords_nonce');
        if (current_user_can('manage_options') && !empty($_POST['wprt_keywords_input'])) {
            $added = WPRT_DB::add_keywords(sanitize_textarea_field($_POST['wprt_keywords_input']));
            wp_redirect(admin_url('admin.php?page=wp-rank-tracker&added=' . $added));
            exit;
        }
    }

    if (isset($_POST['wprt_action']) && $_POST['wprt_action'] === 'save_settings') {
        check_admin_referer('wprt_settings_nonce');
        if (current_user_can('manage_options')) {
            update_option('wprt_serper_api_key', sanitize_text_field($_POST['wprt_serper_api_key']));
            update_option('wprt_target_domain', sanitize_text_field($_POST['wprt_target_domain']));
            update_option('wprt_target_region', sanitize_text_field($_POST['wprt_target_region']));
            update_option('wprt_target_language', sanitize_text_field($_POST['wprt_target_language']));
            wp_redirect(admin_url('admin.php?page=wp-rank-tracker-settings&saved=1'));
            exit;
        }
    }
});

// Render Dashboard View
function wprt_render_dashboard_page() {
    $keywords = WPRT_DB::get_all_keywords();
    $total_kw = count($keywords);

    $top3 = 0;
    $top10 = 0;
    $unranked = 0;

    foreach ($keywords as $kw) {
        if ($kw->current_rank !== null && $kw->current_rank > 0) {
            if ($kw->current_rank <= 3) $top3++;
            if ($kw->current_rank <= 10) $top10++;
        } else {
            $unranked++;
        }
    }

    $target_domain = get_option('wprt_target_domain', '');
    $region = strtoupper(get_option('wprt_target_region', 'in'));
    ?>
    <div class="wrap wprt-wrap">
        <div class="wprt-header">
            <div>
                <h1>📈 Unrestricted Google Rank Tracker</h1>
                <p style="margin: 4px 0 0 0; color: #646970;">
                    Target Domain: <strong><?php echo !empty($target_domain) ? esc_html($target_domain) : '<span style="color:#d63638;">Not configured yet (Set in Settings)</span>'; ?></strong> | Region: <strong>Google <?php echo esc_html($region); ?></strong>
                </p>
            </div>
            <div>
                <a href="<?php echo esc_url(admin_url('admin.php?page=wp-rank-tracker-settings')); ?>" class="button button-secondary">⚙ Settings</a>
                <a href="<?php echo esc_url(admin_url('admin-post.php?action=wprt_export_csv')); ?>" class="button button-secondary">📥 Export CSV</a>
                <button type="button" id="wprt-btn-check-all" class="button button-primary">▶ Check All Rankings Now</button>
            </div>
        </div>

        <div style="background: #e7f3fe; border-left: 4px solid #2271b1; padding: 12px 18px; margin-bottom: 20px; border-radius: 4px; font-size: 13px; color: #1d2327;">
            💡 <strong>Front-End Public Tool:</strong> Want visitors or clients to use this rank tracker on your website? Paste the shortcode <code>[google_rank_tracker]</code> into any page or post!
        </div>

        <?php if (isset($_GET['added'])): ?>
            <div class="notice notice-success is-dismissible">
                <p>Successfully added <?php echo intval($_GET['added']); ?> keyword(s)!</p>
            </div>
        <?php endif; ?>

        <!-- Stat Cards -->
        <div class="wprt-stats">
            <div class="wprt-stat-card">
                <div class="wprt-stat-title">Total Keywords</div>
                <div class="wprt-stat-num"><?php echo $total_kw; ?></div>
            </div>
            <div class="wprt-stat-card top3">
                <div class="wprt-stat-title">Top 3 Rankings (#1-#3)</div>
                <div class="wprt-stat-num" style="color: #008a00;"><?php echo $top3; ?></div>
            </div>
            <div class="wprt-stat-card top10">
                <div class="wprt-stat-title">Top 10 Rankings (#1-#10)</div>
                <div class="wprt-stat-num" style="color: #2e7d32;"><?php echo $top10; ?></div>
            </div>
            <div class="wprt-stat-card unranked">
                <div class="wprt-stat-title">Unranked / Beyond 100</div>
                <div class="wprt-stat-num" style="color: #646970;"><?php echo $unranked; ?></div>
            </div>
        </div>

        <!-- Add Keywords Card -->
        <div class="wprt-card">
            <h2>Add Keywords</h2>
            <form method="post" action="">
                <?php wp_nonce_field('wprt_add_keywords_nonce'); ?>
                <input type="hidden" name="wprt_action" value="add_keywords">
                <p style="margin: 0 0 8px 0; color: #646970; font-size: 13px;">Enter keywords below (one per line, or comma-separated):</p>
                <textarea name="wprt_keywords_input" rows="3" style="width: 100%; max-width: 800px; font-size: 13px;" placeholder="Enter keywords here (one per line)..."></textarea>
                <p style="margin-top: 10px;">
                    <button type="submit" class="button button-primary">+ Add Keywords</button>
                </p>
            </form>
        </div>

        <!-- Progress Bar -->
        <div id="wprt-progress-container" class="wprt-progress-container">
            <div id="wprt-progress-bar" class="wprt-progress-bar"></div>
        </div>
        <div id="wprt-progress-text" class="wprt-progress-text" style="display:none;"></div>

        <!-- Keywords Table -->
        <div class="wprt-card" style="padding: 0; overflow: hidden;">
            <table class="wprt-table">
                <thead>
                    <tr>
                        <th style="width: 40px; text-align: center;">#</th>
                        <th>Keyword</th>
                        <th style="width: 130px;">Google Rank</th>
                        <th>Ranked Landing Page URL</th>
                        <th style="width: 160px;">Last Checked</th>
                        <th style="width: 140px; text-align: right;">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (empty($keywords)): ?>
                        <tr>
                            <td colspan="6" style="text-align: center; padding: 30px; color: #8c8f94;">
                                No keywords added yet. Use the box above to add your first keywords!
                            </td>
                        </tr>
                    <?php else: ?>
                        <?php $idx = 1; foreach ($keywords as $kw): ?>
                            <tr id="wprt-row-<?php echo $kw->id; ?>" class="wprt-keyword-row" data-id="<?php echo $kw->id; ?>">
                                <td style="text-align: center; color: #8c8f94; font-weight: 500;"><?php echo $idx++; ?></td>
                                <td style="font-weight: 600; color: #1d2327;">
                                    <?php echo esc_html($kw->keyword); ?>
                                </td>
                                <td class="wprt-col-rank">
                                    <?php
                                    if ($kw->current_rank !== null && $kw->current_rank > 0) {
                                        $r = intval($kw->current_rank);
                                        $cls = 'wprt-badge-top100';
                                        if ($r <= 3) $cls = 'wprt-badge-top3';
                                        elseif ($r <= 10) $cls = 'wprt-badge-top10';
                                        elseif ($r <= 20) $cls = 'wprt-badge-top20';
                                        elseif ($r <= 50) $cls = 'wprt-badge-top50';
                                        echo '<span class="wprt-badge ' . $cls . '">' . $r . '</span> ';

                                        if ($kw->previous_rank !== null && $kw->previous_rank > 0) {
                                            $diff = intval($kw->previous_rank) - $r;
                                            if ($diff > 0) {
                                                echo '<span class="wprt-change-up">▲ +' . $diff . '</span>';
                                            } elseif ($diff < 0) {
                                                echo '<span class="wprt-change-down">▼ ' . $diff . '</span>';
                                            } else {
                                                echo '<span class="wprt-change-same">— 0</span>';
                                            }
                                        }
                                    } else {
                                        echo '<span class="wprt-badge wprt-badge-unranked">-</span>';
                                    }
                                    ?>
                                </td>
                                <td class="wprt-col-url">
                                    <?php if (!empty($kw->ranked_url) && $kw->current_rank !== null): ?>
                                        <a href="<?php echo esc_url($kw->ranked_url); ?>" target="_blank" class="wprt-url" title="<?php echo esc_attr($kw->ranked_url); ?>">
                                            <?php echo esc_html($kw->ranked_url); ?>
                                        </a>
                                    <?php else: ?>
                                        <span style="color: #8c8f94;">Not ranked</span>
                                    <?php endif; ?>
                                </td>
                                <td class="wprt-col-date" style="color: #646970; font-size: 12px;">
                                    <?php echo $kw->last_checked ? esc_html($kw->last_checked) : 'Never'; ?>
                                </td>
                                <td style="text-align: right;">
                                    <button type="button" class="button button-small wprt-btn-check-single" data-id="<?php echo $kw->id; ?>">Check</button>
                                    <button type="button" class="button button-small button-link-delete wprt-btn-delete" data-id="<?php echo $kw->id; ?>" style="color: #d63638; margin-left: 5px;">Delete</button>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
    <?php
}

// Render Settings View
function wprt_render_settings_page() {
    $api_key = get_option('wprt_serper_api_key', '499a4c6f466313cc4dadb69021321bfb14547034');
    $domain  = get_option('wprt_target_domain', '');
    $region  = get_option('wprt_target_region', 'in');
    $lang    = get_option('wprt_target_language', 'en');
    ?>
    <div class="wrap wprt-wrap">
        <h1>⚙ Rank Tracker Settings</h1>

        <?php if (isset($_GET['saved'])): ?>
            <div class="notice notice-success is-dismissible">
                <p>Settings saved successfully!</p>
            </div>
        <?php endif; ?>

        <div class="wprt-card" style="max-width: 700px;">
            <form method="post" action="">
                <?php wp_nonce_field('wprt_settings_nonce'); ?>
                <input type="hidden" name="wprt_action" value="save_settings">

                <table class="form-table">
                    <tr>
                        <th scope="row"><label for="wprt_serper_api_key">Serper.dev API Key</label></th>
                        <td>
                            <input type="text" name="wprt_serper_api_key" id="wprt_serper_api_key" value="<?php echo esc_attr($api_key); ?>" class="regular-text" required>
                            <p class="description">Your API key from <a href="https://serper.dev" target="_blank">serper.dev</a> (2,500 free queries).</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="wprt_target_domain">Target Website Domain</label></th>
                        <td>
                            <input type="text" name="wprt_target_domain" id="wprt_target_domain" value="<?php echo esc_attr($domain); ?>" class="regular-text" placeholder="e.g. yourdomain.com">
                            <p class="description">The website domain you want to track (e.g. <code>yourdomain.com</code>).</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="wprt_target_region">Target Google Country / Region</label></th>
                        <td>
                            <select name="wprt_target_region" id="wprt_target_region">
                                <option value="in" <?php selected($region, 'in'); ?>>India (in)</option>
                                <option value="us" <?php selected($region, 'us'); ?>>United States (us)</option>
                                <option value="uk" <?php selected($region, 'uk'); ?>>United Kingdom (uk)</option>
                                <option value="ca" <?php selected($region, 'ca'); ?>>Canada (ca)</option>
                                <option value="au" <?php selected($region, 'au'); ?>>Australia (au)</option>
                                <option value="sg" <?php selected($region, 'sg'); ?>>Singapore (sg)</option>
                                <option value="ae" <?php selected($region, 'ae'); ?>>United Arab Emirates (ae)</option>
                            </select>
                            <p class="description">Google localized search country index.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="wprt_target_language">Target Search Language</label></th>
                        <td>
                            <select name="wprt_target_language" id="wprt_target_language">
                                <option value="en" <?php selected($lang, 'en'); ?>>English (en)</option>
                                <option value="hi" <?php selected($lang, 'hi'); ?>>Hindi (hi)</option>
                                <option value="bn" <?php selected($lang, 'bn'); ?>>Bengali (bn)</option>
                                <option value="es" <?php selected($lang, 'es'); ?>>Spanish (es)</option>
                                <option value="fr" <?php selected($lang, 'fr'); ?>>French (fr)</option>
                            </select>
                        </td>
                    </tr>
                </table>

                <p class="submit">
                    <button type="submit" class="button button-primary">Save Settings</button>
                </p>
            </form>
        </div>
    </div>
    <?php
}
