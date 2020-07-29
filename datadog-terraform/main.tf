variable "DD_API_KEY" {
  type = string
}

variable "DD_APP_KEY" {
  type = string
}

# Configure the Datadog provider
provider "datadog" {
  api_key = "${var.DD_API_KEY}"
  app_key = "${var.DD_APP_KEY}"
}

resource "datadog_monitor" "login_failures" {
  name               = "Login Failures are High"
  type               = "query alert"
  message            = "{{#is_alert}}\nThe last time we experienced a high number of failed logins it was because we broke the authentication controller. \n{{/is_alert}}"
  escalation_message = "Escalation message @pagerduty"

  query = "sum(last_5m):avg:login{outcome:failure}.as_count() > 100"

  thresholds = {
    critical          = 100
  }

  notify_no_data    = false
  renotify_interval = 60

  notify_audit = false
  timeout_h    = 60
  include_tags = true

}