#include "ext-idle-notify-v1-client-protocol.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <wayland-client.h>

static struct wl_display *display = NULL;
static struct wl_registry *registry = NULL;
static struct wl_seat *seat = NULL;
static struct ext_idle_notifier_v1 *idle_notifier = NULL;
static struct ext_idle_notification_v1 *idle_notification = NULL;

static void idle_handle_idle(void *data,
                             struct ext_idle_notification_v1 *notification) {
  printf("idle\n");
  fflush(stdout);
}

static void idle_handle_resumed(void *data,
                                struct ext_idle_notification_v1 *notification) {
  printf("resume\n");
  fflush(stdout);
}

static const struct ext_idle_notification_v1_listener idle_listener = {
    .idled = idle_handle_idle,
    .resumed = idle_handle_resumed,
};

static void registry_add(void *data, struct wl_registry *registry,
                         uint32_t name, const char *interface,
                         uint32_t version) {
  if (strcmp(interface, "ext_idle_notifier_v1") == 0) {
    idle_notifier =
        wl_registry_bind(registry, name, &ext_idle_notifier_v1_interface, 1);
  } else if (strcmp(interface, "wl_seat") == 0) {
    seat = wl_registry_bind(registry, name, &wl_seat_interface, 1);
  }
}

static void registry_remove(void *data, struct wl_registry *registry,
                            uint32_t name) {}

static const struct wl_registry_listener registry_listener = {registry_add,
                                                              registry_remove};

int main(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "Usage: %s <timeout_ms>\n", argv[0]);
    return 1;
  }

  int timeout = atoi(argv[1]);

  display = wl_display_connect(NULL);
  if (!display) {
    fprintf(stderr, "Failed to connect to Wayland\n");
    return 1;
  }

  registry = wl_display_get_registry(display);
  wl_registry_add_listener(registry, &registry_listener, NULL);
  wl_display_roundtrip(display);

  if (!idle_notifier) {
    fprintf(stderr, "Idle notifier not supported\n");
    return 1;
  }

  if (!seat) {
    fprintf(stderr, "No wl_seat found\n");
    return 1;
  }

  idle_notification =
      ext_idle_notifier_v1_get_idle_notification(idle_notifier, timeout, seat);

  ext_idle_notification_v1_add_listener(idle_notification, &idle_listener,
                                        NULL);

  while (wl_display_dispatch(display) != -1) {
  }

  return 0;
}
