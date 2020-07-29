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

resource "datadog_dashboard" "ordered_dashboard" {
  title         = "Our Custom Login Dashboard"
  description   = "This dashboard dispalys ALL of the data we need to visualize and debug issues with our custom login functionality."
  layout_type   = "ordered"

  widget {
    timeseries_definition {
      request {
        q = "sum:login{*} by {outcome}.as_count()"
        display_type = "line"
        style {
          palette = "warm"
          line_type = "solid"
          line_width = "normal"
        }
      }
      title = "Logins by Outcome"
    }
  }

  widget {
    query_value_definition {
      request {
        q = "sum:login{outcome:success}.as_count()"
        aggregator = "sum"
      }
      title = "Successful Logins"
    }
  }
  widget {
    query_value_definition {
      request {
        q = "sum:login{outcome:failure}.as_count()"
        aggregator = "sum"
      }
      title = "Failed Logins"
    }
  }
}


resource "datadog_logs_custom_pipeline" "flask_pipeline" {
    filter {
        query = "service:securityworkshop_server"
    }
    name = "Flask"
    is_enabled = true

    processor {
        grok_parser {
            samples = [
              "INFO:werkzeug:93.3.245.83 - - [21/Jul/2020 02:21:22] \"[37mPOST /login HTTP/1.1[0m\" 200 -"
            ]
            source = "message"
            grok {
                support_rules = ""
                match_rules = <<EOT
# python does weird color encoding so you will see some odd things in here like `\[%%{integer}m`

httpRule INFO:werkzeug:%%{ipv4:network.client.ip} - - \[%%{date("dd/MMM/yyyy HH:mm:ss"):date}\] \"%%{data}%%{regex("POST|GET|PUT|DELETE|PATCH"):http.method} %%{notSpace:http.url} %%{notSpace:http.version}\[%%{integer}m\" %%{integer:http.status_code} -

logRule %%{word:level}:%%{notSpace:logHandler}:%%{data::keyvalue}
EOT
            }
            name = "Flask Grok parser"
            is_enabled = true
        }
    }
    processor {
        date_remapper {
            sources = ["date"]
            is_enabled = true
        }
    }

    processor {
        url_parser {
            sources = ["http.url"]
            target = "http.url_dtailsl"
            is_enabled = true
        }
    }
    processor {
        category_processor {
            target = "http.status_category"
            category {
                name = "OK"
                filter {
                    query = "@http.status_code[200 TO 299]"
                }
            }
            category {
                name = "notice"
                filter {
                    query = "@http.status_code[300 TO 399]"
                }
            }
            category {
                name = "warning"
                filter {
                    query = "@http.status_code[400 TO 499]"
                }
            }
            name = "HTTP Status Code to Category"
            is_enabled = true
        }
    }
    processor {
          status_remapper {
              sources = ["http.status_category"]
              is_enabled = true
          }
      }
}