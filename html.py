
def write_header(rh, p=20, m=10, pb=0):
    rh.response.out.write("""
<html>
  <head>
    <title>Color Quest</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
  </head>
  <body>
  <div id="wrap" style="margin-top:%dpx; margin-bottom: %dpx; padding:0 %dpx %dpx %dpx">
""" % (m, m, p, pb, p))

def write_footer(rh):
    rh.response.out.write('</div></body></html>')
