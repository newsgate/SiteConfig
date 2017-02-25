# coding=utf-8

import random
import search_intr
import el
import search_util
import time

show_counters = True
source_recommendation_link = True

BL_TOP_BAR = 0x1
BL_COPYRIGHT_BAR = 0x2

blog_link = BL_COPYRIGHT_BAR
participation_link = BL_COPYRIGHT_BAR

show_counters = False
blog_link = 0
participation_link = 0
terms_link = True

class Interceptor(search_intr.Interceptor):

  interceptor_base = search_intr.Interceptor

  def __init__(this, context, logger, page_id, render):

    this.interceptor_base.__init__(this, context, logger, render, __file__)
    
    request = context.request
    this.page = page_id == None and request.uri() or page_id

    this.page_shared = False
    this.has_adult_content = None

  def bastion(this, service):

#    return ""

    request = this.context.request
    render = this.render()

    log = False
    log_headers = False
    unavailable = False
    slowdown = 0

    header = request.input.headers().find
    ua = header("user-agent")
    ref = header("referer")
    cookie = header("cookie")
    unparsed_uri = request.unparsed_uri()
    start_from = render.start_from
    results = render.results_per_page

    url_prefix = "/p/s/h?n=eng&v=S"
    test_uid = "1B55EA1081B9B04C2091D2F729A36054__"

    block = ""

    try:
      if render.uid == "A860620EE83C5D4EEA889F562618A0E6" or \
         render.uid == test_uid:
        block = "!UID!"

      if not block and \
         ua == "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.16" and \
         unparsed_uri[0:len(url_prefix)] == url_prefix:
        render.start_from = 0
        render.results_per_page = 1
        block = "!URL!"
    except:
      pass

    if log:
      this.logger.trace(el.logging.HIGH, "Bastion", block or "-", " ", service,
                        " *IP=", request.remote_ip(), " *STR=", start_from,
                        " *RES=", results,
                        " *URL=", unparsed_uri,
                        " *REF=", ref, " *UA=", ua, " *CK=", cookie)

      if log_headers:
        for h in request.input.headers():
          this.logger.trace(el.logging.HIGH, "Bastion", " HDR ", 
                            request.remote_ip(), " ", h.name, ":", h.value)

    if block:
      if unavailable: render.exit(503) #service unavailable
      if slowdown: time.sleep(slowdown)

    return block

  def blog_url(this):
    
    link = "http://newsfiber.blogspot.ru"

    translator = this.render().default_translator
    
    if translator and translator.to_lang.l3_code() != "rus":
      link = translator.enrich_outer_link(link)

    return link
  
  def counters(this, category_path):

    if not show_counters: return None

    text = R'''
<!--LiveInternet counter--><script type="text/javascript"><!--
document.write("<a href='http://www.liveinternet.ru/click' "+
"target=_blank><img src='//counter.yadro.ru/hit?t26.3;r"+
escape(document.referrer)+((typeof(screen)=="undefined")?"":
";s"+screen.width+"*"+screen.height+"*"+(screen.colorDepth?
screen.colorDepth:screen.pixelDepth))+";u"+escape(document.URL)+
";"+Math.random()+
"' alt='' title='LiveInternet: показано число посетителей за"+
" сегодня' "+
"border='0' width='88' height='13'><\/a>")
//--></script><!--/LiveInternet-->
'''

    is_space = (this.page == "search" or this.page == "/p/s/h") and \
        category_path != None and category_path.find("/Science/Space") == 0

    is_space = False
    
    if is_space:
      text += R'''
<!--Openstat--><span id="openstat2106209"></span><script type="text/javascript">
var openstat = { counter: 2106209, image: 5061, next: openstat, track_links: "all" }; document.write(unescape("%3Cscript%20src=%22http" +
(("https:" == document.location.protocol) ? "s" : "") +
"://openstat.net/cnt.js%22%20defer=%22defer%22%3E%3C/script%3E"));
</script><!--/Openstat-->

<!--Rating@Mail.ru counter-->
<script language="javascript"><!--
d=document;var a='';a+=';r='+escape(d.referrer);js=10;//--></script>
<script language="javascript1.1"><!--
a+=';j='+navigator.javaEnabled();js=11;//--></script>
<script language="javascript1.2"><!--
s=screen;a+=';s='+s.width+'*'+s.height;
a+=';d='+(s.colorDepth?s.colorDepth:s.pixelDepth);js=12;//--></script>
<script language="javascript1.3"><!--
js=13;//--></script><script language="javascript" type="text/javascript"><!--
d.write('<a href="http://top.mail.ru/jump?from=1867412" target="_top">'+
'<img src="http://de.c7.bc.a1.top.mail.ru/counter?id=1867412;t=84;js='+js+
a+';rand='+Math.random()+'" alt="-LÀÕÙâØÝÓ@Mail.ru" border="0" '+
'height="18" width="88"><\/a>');if(11<js)d.write('<'+'!-- ');//--></script>
<noscript><a target="_top" href="http://top.mail.ru/jump?from=1867412">
<img src="http://de.c7.bc.a1.top.mail.ru/counter?js=na;id=1867412;t=84" 
height="18" width="88" border="0" alt="ÀÕÙâØÝÓ@Mail.ru"></a></noscript>
<script language="javascript" type="text/javascript"><!--
if(11<js)d.write('--'+'>');//--></script>
<!--// Rating@Mail.ru counter-->
'''

    return text
  
  def footer_anchors(this):

    res = []
    uri = this.context.request.uri()

    if source_recommendation_link and uri != "/p/x/r":
      res.append('<a target="_blank" href="/p/x/r">' + \
                 this.localization("SOURCE_RECOMMENDATION") + '</a>')

    if (participation_link & BL_COPYRIGHT_BAR) and uri != "/p/x/p":
      res.append('<a target="_blank" href="/p/x/p">' + \
                 this.localization("PROJECT_PARTICIPATION") + '</a>')

    if blog_link & BL_COPYRIGHT_BAR:
      res.append('<a target="_blank" href="' + this.blog_url() + '">' + \
                 this.localization("BLOG") + '</a>')

    if terms_link and uri != "/p/x/u":
      res.append('<a target="_blank" href="/p/x/u">' + \
                 this.localization("TERMS_OF_USE") + '</a>')
    
    return res

  def share_page(this):

    if this.render().search_result == None or \
       len(this.render().search_result.messages) == 0:
      return ""

    this.page_shared = True
   
    if this.render().site_version == search_util.SearchPageContext.SV_MOB:
      
      add_this_style = " addthis_32x32_style"
      width1 = "115px"
      width2 = "115"
      height2 = "32"

      buttons = R'''
<a class="addthis_button_preferred_1"></a>
<a class="addthis_button_preferred_2"></a>
<a class="addthis_button_compact"></a>'''
      
    else:
      
      add_this_style = ""
      width1 = "15em"
      width2 = "85"
      height2 = "16"

      buttons = R'''
<a class="addthis_button_preferred_1"></a>
<a class="addthis_button_preferred_2"></a>
<a class="addthis_button_preferred_3"></a>
<a class="addthis_button_compact"></a>'''
      
    text = R'''<table style="font-size:100%;border-collapse:collapse;padding:0;margin:0;" cellspacing="0">
<tr style="padding:0;margin:0">'''

    if this.render().site_version != search_util.SearchPageContext.SV_MOB:
      text += '<td style="padding:0;margin:0;white-space:nowrap;">' + \
              this.localization("SHARE") + '</td>'

    text += R'''
<td style="width:''' + width1 + \
           R''';padding:0;margin:0;white-space:nowrap">
<table style="table-layout:fixed;width:''' + width2 + \
           R'''px;border-collapse:collapse;padding:0;margin:0;" cellspacing="0">
<tr><td style="padding:0;margin:0;white-space:nowrap;height:''' + height2 + \
           R'''px;">
<script type="text/javascript">
var addthis_config =
{
   pubid : "xa-4fc67487252866eb",
   ui_delay : 500,
   ui_offset_left : 30,
   ui_language: "''' + this.context.request.input.lang.l3_code() + \
           R'''"
}

function initAddThis()
{
  addthis.init();
}
</script>    
<!-- AddThis Button BEGIN -->
<div class="addthis_toolbox addthis_default_style''' + \
           add_this_style + '">' + buttons + \
           R'''
<!-- <a class="addthis_counter addthis_bubble_style"></a> -->
</div>
<script type="text/javascript" src="http://s7.addthis.com/js/250/addthis_widget.js#async=1"></script>
<!-- AddThis Button END --></td></tr></table></td></tr></table>'''

    return text

  def body(this):

    if this.page_shared:
      return R'''<script type="text/javascript">
initAddThis();
</script>'''
    
    return None

  def adult_content(this):

    plus18 = False
    
    if this.render().search_result != None:
      
      for msg in this.render().search_result.messages:

        for cat in msg.categories:
          if cat[0:12] == "/Society/18+":
            plus18 = True
            break
            
        if plus18: break

    return plus18

  def page_marker(this):

    if this.adult_content():
  
      browser = this.render().browser

      style = this.render().site_version == \
        search_util.SearchPageContext.SV_MOB and \
        "margin:0 0.15em 0 0" or "margin:0 0 0 1em"
      
      return '<img src="' + \
             this.render().resource_url('/18plus.png') + \
             '" width="30" height="16" style="vertical-align:' + \
           (browser == "msie" and "top" or "top") + \
           '; ' + style + '"/>'

    return None
  
  def max_thumb(this, msg, max_thumb):
  
    images = []
    if msg.front_image: images.append(msg.front_image)
    for img in msg.images: images.append(img)
          
    for img in images:
      for thumb in img.thumbs:
        if max_thumb == None or thumb.width > max_thumb.width or \
           thumb.width == max_thumb.width and \
           thumb.height > max_thumb.height:
          
          max_thumb = thumb

    return max_thumb

  def head(this):

    result = ''
    
    if this.render() != None and (this.page == "/p/s/h" or \
       this.page == "/p/s/m" or this.page == "/"):

      message_article = this.page == "/p/s/m"

      article = this.page == "/p/s/h" and \
                this.render().modifier.similar.message_id or \
                message_article

      
      if article:
        if result: result += '\n'
        result += '<meta property="og:type" content="article"/>'

      title = this.page == "/" and \
                el.string.manip.xml_encode(\
                  this.render().static.server_instance_name) or \
                this.render().query_title()

      if title:
        if result: result += '\n'    
        result += '<meta property="og:title" content="' + title + '"/>'

      description = ""
      max_thumb = None

      if article:
        try:

          msg = this.render().search_result.messages[0]
          
          description = \
            el.string.manip.xml_encode(\
              search_util.truncate_text(\
                el.string.manip.xml_decode(msg.description),
                200))

          max_thumb = this.max_thumb(msg, max_thumb)
          
        except:
          pass

      if description:
        if result: result += '\n'
        
        result += '<meta property="og:description" content="' + \
                  description + '"/>'


      extras = message_article and \
               ("msg=" + el.string.manip.mime_url_encode(msg.encoded_id)) or ""
      
      result += '\n<meta property="og:url" content="' + \
                el.string.manip.xml_encode(\
                  this.render().search_link(export=True, extra_params=extras))+\
                '"/>'

      if max_thumb == None:
        try:
          for msg in this.render().search_result.messages:
            max_thumb = this.max_thumb(msg, max_thumb)

        except:
          pass

      if max_thumb != None:
        src = el.string.manip.xml_encode(max_thumb.src)
        result += '\n<meta property="og:image" content="' + src + \
                  '"/>\n<link rel="image_src" href="' + src + '">'

    if result: result += '\n'

    result += R'''<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-32182971-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>'''

    return result

  def top_bar_menu(this, pos, id):

    if id != "end" or \
       this.render().site_version == search_util.SearchPageContext.SV_MOB:
      return None
      
    menu = ""
    
    if (participation_link & BL_TOP_BAR) and \
       this.context.request.uri() != "/p/x/p":
      menu += '<a target="_blank" href="/p/x/p">' + \
              this.localization("PROJECT_PARTICIPATION") + '</a>'

    if (blog_link & BL_TOP_BAR):
      
      if menu: menu += " | "
      
      menu += '<a target="_blank" href="' + this.blog_url() + '">' + \
              this.localization("BLOG") + '</a>'
      
    return menu

def create_interceptor(context, logger, page_id = None, render = None):
  return Interceptor(context, logger, page_id, render)
