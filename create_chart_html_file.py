
# https://www.tradingview.com/widget/advanced-chart/

background_color = "#0f1c30"
timezone         = "Europe/Berlin"

# exchanges: COINBASE, BINANCE, BITTREX, :VENBTC
symbols          = ["COINBASE:BTCUSD", "COINBASE:ETHUSD", "COINBASE:LTCUSD",
                    "BINANCE:NEOUSDT", "BINANCE:NANOETH", "BITTREX:ADAUSDT",
                    "BINANCE:VENBTC", "BINANCE:ICXBTC", "BINANCE:REQBTC"]
columns			 = 3
screen_width     = 1920
screen_height    = 1000

interval         = 15 # 1, 3, 5, 15, 30, 60, 240
theme            = "Dark"

rows             = int(len(symbols)/columns)

widget_width     = int((screen_width*1)/columns)
widget_height    = int((screen_height*0.92)/rows)
print("widget_width: " ,widget_width)
print("widget_height:",widget_height)

title            = list(set([symbol.split(":")[1] for symbol in symbols]))
title_string     = " ".join(title)

filename_1 = str(columns)+"x"+str(rows)+"_"+"_".join(title)+"_"+str(screen_width)+"x"+str(screen_height)+".html"
filename_2 = "current_portfolio_"+str(screen_width)+"x"+str(screen_height)+".html"

def create_widget_string(symbol, width=widget_width, height=widget_height, interval=interval, theme=theme, timezone=timezone):
    string="""
        <script type="text/javascript">new TradingView.widget({{
          "width": {width},
          "height": {height},
          "symbol": "{symbol}",
          "interval": "{interval}",
          "timezone": "{timezone}",
          "theme": "{theme}",
          "style": "1",
          "locale": "en",
          "toolbar_bg": "#f1f3f6",
          "enable_publishing": false,
          "allow_symbol_change": true,
          "save_image": false,
          "hideideas": true
        }});
        </script>
    """.format(symbol=symbol, width=width, height=height, interval=interval, theme=theme, timezone=timezone)
    return string

string_head="""
<!DOCTYPE html>
<html>
<script type="text/javascript" src="https://s3.tradingview.com/tv.js">
</script>

<head>
  <title>{title}</title>

  <style>
    body {{background-color: {background_color} }}

    .grid {{
      display: table;
      border-spacing: 1px;
      width: 100%
    }}

    .row {{
      display: table-row;
      width: 100%
    }}

    .cell {{
      height: {height}px;
      display: table-cell;
    }}

    }}
  </style>
</head>
""".format(title=title_string, background_color=background_color, height=widget_height)


string_body_start = """
<body>
<div class="grid">
"""

counter = 0
content_string = ' <div class="row">\n'

for symbol in symbols:
    content_string = content_string + '  <div class="cell">' + create_widget_string(symbol) + '</div>\n'
    counter = counter +1
    if (counter%columns == 0) and (counter<len(symbols)):
        content_string = content_string + '  </div>\n  <div class="row">\n'

content_string = content_string + ' </div>'

string_body_end = """
</div>
</body>

</html>
"""



output_string = string_head + string_body_start + content_string + string_body_end

with open(filename_1, "w") as file_html:
    file_html.write(output_string)

with open(filename_2, "w") as file_html:
    file_html.write(output_string)

print("\nsaved files")
