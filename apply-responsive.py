# Re-applies the responsive fixes to a fresh design-tool export of Prototype.dc.html.
# Usage:  python3 -I apply-responsive.py Prototype.dc.html
# Prints "all anchors matched" or lists the markup anchors that moved in the new export.
# NOTE: the release-row and protocol-chip rules plus the "move CSS to end of <style>" step
#       were added after this script; see git history of Prototype.dc.html for those.

import sys, re
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
fails = []

def rep(name, old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        fails.append(f"{name}: expected {count}, got {n}")
        return
    s = s.replace(old, new)

rep('viewport', '<meta charset="utf-8">\n', '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n')
rep('root', '<div class="ui" style="width: 1440px; height: 960px; background: #F3F5F8; position: relative; overflow: hidden; display: flex; flex-direction: column">',
    '<div class="ui shell" style="width: 100%; min-height: 100vh; background: #F3F5F8; position: relative; display: flex; flex-direction: column">')
rep('page', '<div style="flex: 1; padding: 36px 48px; display: flex; flex-direction: column; gap: 24px">',
    '<div class="page" style="flex: 1; padding: 36px 48px; display: flex; flex-direction: column; gap: 24px">')
rep('agrid-hd', '<div style="display: grid; grid-template-columns: 2fr 1.2fr 1.6fr 1fr; gap: 16px; padding: 12px 20px;',
    '<div class="agrid hd" style="display: grid; grid-template-columns: 2fr 1.2fr 1.6fr 1fr; gap: 16px; padding: 12px 20px;')
rep('agrid', '<div style="display: grid; grid-template-columns: 2fr 1.2fr 1.6fr 1fr; gap: 16px; padding: 16px 20px; align-items: center">',
    '<div class="agrid" style="display: grid; grid-template-columns: 2fr 1.2fr 1.6fr 1fr; gap: 16px; padding: 16px 20px; align-items: center">')
rep('overlay', '<div style="position: absolute; inset: 0; background: rgba(20,30,48,.58); display: flex; align-items: flex-start; justify-content: center; padding-top: 40px">',
    '<div class="ovl" style="position: fixed; inset: 0; background: rgba(20,30,48,.58); display: flex; align-items: flex-start; justify-content: center; padding: 24px 16px; overflow-y: auto">')
rep('modal', '<div style="width: 1200px; height: 880px; background: #fff;',
    '<div class="modal" style="width: min(1200px, 100%); min-height: min(700px, 100%); max-height: 100%; background: #fff;')
rep('mhead', '<div style="height: 60px; background: #1C3A6B; display: flex; align-items: center; gap: 14px; padding: 0 16px 0 28px; flex-shrink: 0">',
    '<div class="mhead" style="height: 60px; background: #1C3A6B; display: flex; align-items: center; gap: 14px; padding: 0 16px 0 28px; flex-shrink: 0">')
rep('mname', '<span style="width: 1px; height: 20px; background: rgba(255,255,255,.25)"></span>\n<span style="font-size: 14px; color: rgba(255,255,255,.8)">{{ nameOrPlaceholder }}</span>',
    '<span class="mname" style="width: 1px; height: 20px; background: rgba(255,255,255,.25)"></span>\n<span class="mname" style="font-size: 14px; color: rgba(255,255,255,.8)">{{ nameOrPlaceholder }}</span>')
rep('stepper', '<div style="height: 64px; border-bottom: 1px solid #E5E8EE; background: #F7F8FA; display: flex; align-items: center; padding: 0 48px; flex-shrink: 0" role="list" aria-label="Steps">',
    '<div class="stepper" style="height: 64px; border-bottom: 1px solid #E5E8EE; background: #F7F8FA; display: flex; align-items: center; padding: 0 48px; flex-shrink: 0" role="list" aria-label="Steps">')
rep('dwrap', '<div style="background: #F2F8F3; border-bottom: 1px solid #D9E6DC; padding: 0 20px 0 28px; display: flex; flex-direction: column; flex-shrink: 0">',
    '<div class="dwrap" style="background: #F2F8F3; border-bottom: 1px solid #D9E6DC; padding: 0 20px 0 28px; display: flex; flex-direction: column; flex-shrink: 0">')
rep('dstrip', '<div style="display: flex; align-items: center; gap: 12px; height: 52px">',
    '<div class="dstrip" style="display: flex; align-items: center; gap: 12px; height: 52px">')
rep('dstages', '<sc-if value="{{ stagesOpen }}" hint-placeholder-val="{{ false }}">\n<div style="display: flex; flex-direction: column; gap: 14px; padding: 2px 0 18px">',
    '<sc-if value="{{ stagesOpen }}" hint-placeholder-val="{{ false }}">\n<div class="dstages" style="display: flex; flex-direction: column; gap: 14px; padding: 2px 0 18px">')
rep('plegend', '<div style="display: flex; gap: 20px; font-size: 12.5px; color: #374151">',
    '<div class="plegend" style="display: flex; gap: 20px; font-size: 12.5px; color: #374151">', 2)
rep('enav', '<nav aria-label="Sections" style="width: 232px;', '<nav class="enav" aria-label="Sections" style="width: 232px;')
rep('pgwrap', '<sc-if value="{{ showPlayground }}" hint-placeholder-val="{{ false }}">\n<div style="flex: 1; display: flex; min-height: 0">',
    '<sc-if value="{{ showPlayground }}" hint-placeholder-val="{{ false }}">\n<div class="pgwrap" style="flex: 1; display: flex; min-height: 480px">')
rep('pgbar', '<div style="height: 44px; display: flex; align-items: center; gap: 8px; padding: 0 28px; border-bottom: 1px solid #E5E8EE; font-size: 13px; color: #374151; flex-shrink: 0">',
    '<div class="pgbar" style="height: 44px; display: flex; align-items: center; gap: 8px; padding: 0 28px; border-bottom: 1px solid #E5E8EE; font-size: 13px; color: #374151; flex-shrink: 0">')
rep('pgside', '<aside style="width: 320px; flex-shrink: 0; padding: 24px;', '<aside class="pgside" style="width: 320px; flex-shrink: 0; padding: 24px;')
rep('textarea', '<textarea class="in" style="height: 56px" value="{{ draft }}" onChange="{{ onDraft }}" placeholder="Ask the agent something…"></textarea>',
    '<textarea class="in" style="height: 56px" value="{{ draft }}" onChange="{{ onDraft }}" onKeyDown="{{ onDraftKey }}" placeholder="Ask the agent something… (Enter to send, Shift+Enter for a new line)"></textarea>')
rep('onDraftKey', "      onDraft: (e) => this.setState({ draft: e.target.value }),",
    "      onDraft: (e) => this.setState({ draft: e.target.value }),\n      onDraftKey: (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.sendMessage(); } },")
rep('pubwrap', '<div style="flex: 1; min-height: 0; overflow-y: auto; display: flex; justify-content: center; padding: 36px 48px 24px">',
    '<div class="pubwrap" style="flex: 1; min-height: 0; overflow-y: auto; display: flex; justify-content: center; padding: 36px 48px 24px">')
rep('pub800', '<div style="width: 800px; display: flex; flex-direction: column; gap: 22px">\n\n<div style="display: flex; align-items: center; gap: 14px">',
    '<div style="width: 100%; max-width: 800px; display: flex; flex-direction: column; gap: 22px">\n\n<div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap">')
rep('pubtitle', '<div style="display: flex; flex-direction: column; gap: 2px">\n<h3 style="margin: 0; font-size: 20px; font-weight: 600; color: #111827">{{ pubTitle }}</h3>',
    '<div style="display: flex; flex-direction: column; gap: 2px; flex: 1 1 auto; min-width: 0">\n<h3 style="margin: 0; font-size: 20px; font-weight: 600; color: #111827; white-space: nowrap">{{ pubTitle }}</h3>')
old_footer = '<div style="height: 68px; border-top: 1px solid #E5E8EE; background: #fff; display: flex; align-items: center; gap: 12px; padding: 0 28px; flex-shrink: 0">'
n = s.count(old_footer)
if n >= 4:
    s = s.replace(old_footer, old_footer.replace('<div style=', '<div class="mfoot" style='))
else:
    fails.append(f'mfoot: only {n} footers found')
s, n = re.subn(r'<div style="display: grid; grid-template-columns: repeat\(3, minmax\(0, 1fr\)\)',
               '<div class="g3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr))', s)
if n < 1: fails.append('g3: none found')

css = '''
@media (max-width: 1100px){
.page{padding:24px!important}
.stepper{padding:0 24px!important}
.full{padding:24px!important}
}
@media (max-width: 900px){
.enav{display:none!important}
.pgwrap{flex-direction:column!important}
.pgwrap>div:first-child{border-right:0!important;border-bottom:1px solid #E5E8EE;min-height:360px}
.pgside{width:100%!important;max-height:40%}
.g3{grid-template-columns:1fr!important;gap:12px!important}
.dstages{max-height:40vh;overflow-y:auto;padding-right:4px}
.agrid.hd{display:none!important}
.agrid{grid-template-columns:1fr!important;gap:10px!important}
.agrid>div:last-child{justify-content:flex-start!important}
.rv{grid-template-columns:1fr!important;gap:4px!important}
.kv{grid-template-columns:1fr;gap:4px}
.mrow{max-width:90%}
.step{font-size:0;gap:0}
.step .no{font-size:12.5px}
.line{margin:0 8px}
.rlh{flex-wrap:wrap;gap:8px 16px}
.rlh input.in{max-width:none;flex:1 1 100%}
}
@media (max-width: 640px){
.page{padding:20px 16px!important}
.ovl{padding:0!important}
.modal{border-radius:0!important;height:100%!important;min-height:0!important;max-height:100%!important;box-shadow:none!important}
.grid2{grid-template-columns:1fr}
.wiz{padding:24px 16px;gap:28px}
.full{padding:20px 16px!important;gap:28px}
.pgwrap>div:first-child>div{padding-left:16px!important;padding-right:16px!important}
.pgside{padding:16px!important}
.mfoot{height:auto!important;min-height:60px;padding:10px 16px!important;gap:8px!important;flex-wrap:wrap;justify-content:flex-end}
.mfoot .help{display:none}
.mfoot .btn-t{padding:0 6px;font-size:12.5px}
.mfoot .btn{height:36px;padding:0 14px}
.mhead{padding:0 8px 0 16px!important;gap:10px!important}
.mhead h2{white-space:nowrap;font-size:16px}
.mname,.dmeta{display:none!important}
.dstrip{height:auto!important;min-height:44px;flex-wrap:wrap;gap:6px 10px!important;padding:8px 0}
.dwrap{padding:0 16px!important}
.plegend{flex-wrap:wrap;gap:6px 14px!important}
.plegend>span{white-space:nowrap}
.pgbar{height:auto!important;flex-wrap:wrap;padding:8px 16px!important;gap:4px 8px!important;line-height:1.5}
.pubwrap{padding:20px 16px 16px!important}
.rr{flex-wrap:wrap}
.rsel .hd{flex-wrap:wrap}
}
'''
rep('css', '.kv .k{color:#5B6472;font-size:12.5px;font-weight:500}\n', '.kv .k{color:#5B6472;font-size:12.5px;font-weight:500}\n' + css)
open(p, 'w', encoding='utf-8').write(s)
print('FAILED:' if fails else 'all anchors matched'); [print(' -', f) for f in fails]
