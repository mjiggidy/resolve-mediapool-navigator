__VERSION__ = "0.5-dev"
URL_GITHUB  = "https://github.com/mjiggidy/resolve_mediapool_navigator/"
URL_DONATE  = "https://ko-fi.com/lilbinboy/"

from resolvecommon.session import bmd

resolve    = bmd.scriptapp("resolve")
fusion     = bmd.scriptapp("fusion")
ui         = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)