
def write_header(rh, p=20, m=10, pb=0):
    rh.response.out.write("""
<html>
  <head>
    <title>Color Quest</title>
  </head>
  <body style="background-color:#FFFFFF">
  <div style="margin:%dpx auto %dpx auto; padding:0 %dpx %dpx %dpx; width:1000px">
""" % (m, m, p, pb, p))

def write_footer(rh):
    rh.response.out.write('</div></body></html>')
