/*
 * Host-aware 128x32 OLED status screen for the Sol/Luna Corne.
 *
 * The central half retains output, battery, and active-layer status and adds
 * a CAPS badge driven by the host HID indicator report. The peripheral half
 * deliberately retains only split connection and battery status.
 */

#include <lvgl.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/util.h>

#include <dt-bindings/zmk/hid_indicators.h>
#include <zmk/display.h>
#include <zmk/display/status_screen.h>
#include <zmk/display/widgets/battery_status.h>
#include <zmk/display/widgets/layer_status.h>
#include <zmk/display/widgets/output_status.h>
#include <zmk/display/widgets/peripheral_status.h>
#include <zmk/event_manager.h>
#include <zmk/events/hid_indicators_changed.h>
#include <zmk/hid_indicators.h>

#if IS_ENABLED(CONFIG_ZMK_WIDGET_BATTERY_STATUS)
static struct zmk_widget_battery_status battery_status_widget;
#endif

#if IS_ENABLED(CONFIG_ZMK_WIDGET_OUTPUT_STATUS)
static struct zmk_widget_output_status output_status_widget;
#endif

#if IS_ENABLED(CONFIG_ZMK_WIDGET_PERIPHERAL_STATUS)
static struct zmk_widget_peripheral_status peripheral_status_widget;
#endif

#if IS_ENABLED(CONFIG_ZMK_WIDGET_LAYER_STATUS)
static struct zmk_widget_layer_status layer_status_widget;
#endif

#if IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL) && IS_ENABLED(CONFIG_ZMK_HID_INDICATORS)
struct caps_status_state {
    bool active;
};

static lv_obj_t *caps_status_label;

static void caps_status_update_cb(struct caps_status_state state) {
    lv_label_set_text(caps_status_label, state.active ? "CAPS" : "");
}

static struct caps_status_state caps_status_get_state(const zmk_event_t *eh) {
    ARG_UNUSED(eh);

    return (struct caps_status_state){
        .active =
            (zmk_hid_indicators_get_current_profile() & HID_INDICATOR_CAPS_LOCK) != 0,
    };
}

ZMK_DISPLAY_WIDGET_LISTENER(widget_caps_status, struct caps_status_state,
                            caps_status_update_cb, caps_status_get_state)

ZMK_SUBSCRIPTION(widget_caps_status, zmk_hid_indicators_changed);

static void caps_status_init(lv_obj_t *screen) {
    caps_status_label = lv_label_create(screen);
    lv_obj_set_style_text_font(caps_status_label, lv_theme_get_font_small(screen), LV_PART_MAIN);
    lv_obj_align(caps_status_label, LV_ALIGN_BOTTOM_RIGHT, 0, 0);
    widget_caps_status_init();
}
#endif

lv_obj_t *zmk_display_status_screen(void) {
    lv_obj_t *screen = lv_obj_create(NULL);

#if IS_ENABLED(CONFIG_ZMK_WIDGET_BATTERY_STATUS)
    zmk_widget_battery_status_init(&battery_status_widget, screen);
    lv_obj_align(zmk_widget_battery_status_obj(&battery_status_widget), LV_ALIGN_TOP_RIGHT, 0, 0);
#endif

#if IS_ENABLED(CONFIG_ZMK_WIDGET_OUTPUT_STATUS)
    zmk_widget_output_status_init(&output_status_widget, screen);
    lv_obj_align(zmk_widget_output_status_obj(&output_status_widget), LV_ALIGN_TOP_LEFT, 0, 0);
#endif

#if IS_ENABLED(CONFIG_ZMK_WIDGET_PERIPHERAL_STATUS)
    zmk_widget_peripheral_status_init(&peripheral_status_widget, screen);
    lv_obj_align(zmk_widget_peripheral_status_obj(&peripheral_status_widget), LV_ALIGN_TOP_LEFT, 0,
                 0);
#endif

#if IS_ENABLED(CONFIG_ZMK_WIDGET_LAYER_STATUS)
    zmk_widget_layer_status_init(&layer_status_widget, screen);
    lv_obj_set_style_text_font(zmk_widget_layer_status_obj(&layer_status_widget),
                               lv_theme_get_font_small(screen), LV_PART_MAIN);
    lv_obj_align(zmk_widget_layer_status_obj(&layer_status_widget), LV_ALIGN_BOTTOM_LEFT, 0, 0);
#endif

#if IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL) && IS_ENABLED(CONFIG_ZMK_HID_INDICATORS)
    caps_status_init(screen);
#endif

    return screen;
}
