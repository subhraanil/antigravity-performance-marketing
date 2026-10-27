<?php
if (!defined('ABSPATH')) {
    exit;
}

class WPRT_Frontend {

    public static function init() {
        add_shortcode('google_rank_tracker', [__CLASS__, 'render_shortcode']);
        add_shortcode('rank_tracker', [__CLASS__, 'render_shortcode']);
        add_action('wp_enqueue_scripts', [__CLASS__, 'register_assets']);
    }

    public static function register_assets() {
        wp_register_style('wprt-frontend-css', WPRT_PLUGIN_URL . 'assets/css/frontend.css', [], WPRT_VERSION);
        wp_register_script('wprt-frontend-js', WPRT_PLUGIN_URL . 'assets/js/frontend.js', ['jquery'], WPRT_VERSION, true);

        wp_localize_script('wprt-frontend-js', 'wprtFrontData', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce'    => wp_create_nonce('wprt_frontend_nonce')
        ]);
    }

    public static function render_shortcode($atts) {
        $atts = shortcode_atts([
            'max_keywords'   => 15,
            'default_domain' => '',
            'default_region' => get_option('wprt_target_region', 'in'),
            'title'          => 'Free Google Keyword Rank Checker'
        ], $atts, 'google_rank_tracker');

        wp_enqueue_style('wprt-frontend-css');
        wp_enqueue_script('wprt-frontend-js');

        ob_start();
        ?>
        <div class="wprt-front-container" data-max-keywords="<?php echo intval($atts['max_keywords']); ?>">
            <div class="wprt-front-card">
                <div class="wprt-front-header">
                    <h2>🔍 <?php echo esc_html($atts['title']); ?></h2>
                    <p class="wprt-front-subtitle">Check your website's real-time ranking on Google Search with zero limits.</p>
                </div>

                <form id="wprt-front-form">
                    <div class="wprt-front-grid">
                        <div class="wprt-front-field">
                            <label for="wprt_front_domain">Target Website Domain</label>
                            <input type="text" id="wprt_front_domain" placeholder="e.g. yourdomain.com" value="<?php echo esc_attr($atts['default_domain']); ?>" required>
                        </div>
                        <div class="wprt-front-field">
                            <label for="wprt_front_region">Google Region / Country</label>
                            <select id="wprt_front_region">
                                <option value="in" <?php selected($atts['default_region'], 'in'); ?>>India (Google.co.in)</option>
                                <option value="us" <?php selected($atts['default_region'], 'us'); ?>>United States (Google.com)</option>
                                <option value="uk" <?php selected($atts['default_region'], 'uk'); ?>>United Kingdom (Google.co.uk)</option>
                                <option value="ca" <?php selected($atts['default_region'], 'ca'); ?>>Canada (Google.ca)</option>
                                <option value="au" <?php selected($atts['default_region'], 'au'); ?>>Australia (Google.com.au)</option>
                                <option value="sg" <?php selected($atts['default_region'], 'sg'); ?>>Singapore (Google.com.sg)</option>
                                <option value="ae" <?php selected($atts['default_region'], 'ae'); ?>>United Arab Emirates (Google.ae)</option>
                            </select>
                        </div>
                    </div>

                    <div class="wprt-front-field" style="margin-top: 15px;">
                        <label for="wprt_front_keywords">
                            Keywords to Check (up to <?php echo intval($atts['max_keywords']); ?> keywords, one per line)
                        </label>
                        <textarea id="wprt_front_keywords" rows="4" placeholder="Enter keywords here (one per line)..." required></textarea>
                    </div>

                    <div class="wprt-front-actions">
                        <button type="submit" id="wprt-front-submit" class="wprt-front-btn">
                            ▶ Check Google Rankings
                        </button>
                    </div>
                </form>

                <!-- Live Progress Bar -->
                <div id="wprt-front-progress-box" class="wprt-front-progress-box" style="display: none;">
                    <div class="wprt-front-progress-bar-bg">
                        <div id="wprt-front-progress-bar" class="wprt-front-progress-bar"></div>
                    </div>
                    <div id="wprt-front-progress-status" class="wprt-front-progress-status">Scanning 0 of 0 keywords...</div>
                </div>

                <!-- Results Section -->
                <div id="wprt-front-results-box" class="wprt-front-results-box" style="display: none;">
                    <div class="wprt-front-results-header">
                        <h3>📊 Ranking Results</h3>
                        <button type="button" id="wprt-front-export-btn" class="wprt-front-btn-secondary">
                            📥 Download CSV
                        </button>
                    </div>

                    <!-- Summary Chips -->
                    <div class="wprt-front-summary-chips">
                        <div class="wprt-chip">Total: <strong id="wprt-stat-total">0</strong></div>
                        <div class="wprt-chip chip-top3">Top 3: <strong id="wprt-stat-top3">0</strong></div>
                        <div class="wprt-chip chip-top10">Top 10: <strong id="wprt-stat-top10">0</strong></div>
                        <div class="wprt-chip chip-unranked">Not Ranked: <strong id="wprt-stat-unranked">0</strong></div>
                    </div>

                    <div class="wprt-table-responsive">
                        <table class="wprt-front-table">
                            <thead>
                                <tr>
                                    <th style="width: 45px; text-align: center;">#</th>
                                    <th>Keyword</th>
                                    <th style="width: 140px; text-align: center;">Google Rank</th>
                                    <th>Ranked Landing Page URL</th>
                                </tr>
                            </thead>
                            <tbody id="wprt-front-results-body">
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <?php
        return ob_get_clean();
    }
}
