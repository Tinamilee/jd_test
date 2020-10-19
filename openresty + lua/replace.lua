-- 获取单次返回体的数据ngx.arg[1]，ngx.arg[2]标志位，为true时，返回结束。
-- 当返回体数据偏大时，单个请求会有多次返回。
local chunk, eof = ngx.arg[1], ngx.arg[2]
local buffered = ngx.ctx.buffered
if not buffered then
   buffered = {}
   ngx.ctx.buffered = buffered
end
if chunk ~= "" then
   -- 存储每次返回的数据，加入到buffered，
   -- #buffered是获取buffered的长度。数据类型是table：数组/字典组合。
   buffered[#buffered+1] = chunk
   ngx.arg[1] = nil
end

function stringToTable(str)
   local ret = loadstring("return "..str)()
   return ret
end

if eof then
   -- 连接每次返回的数据
   local whole = table.concat(buffered)
   ngx.ctx.buffered = nil
   local tab = nil
   if whole == nil or type(whole) ~= "string" then
      whole = "this is nil or not string "
   else
      package.path = package.path.."/export/serveres/nginx/nginx/lua/?.lua;;"
      package.cpath = package.cpath.."/usr/local/lib/?.so;"
      package.cpath = package.cpath.."/export/serveres/nginx/lualib/?.so;"
      package.cpath = package.cpath.."/export/serveres/nginx/luajit/lib/?.so;"
      
      local ok,errors = pcall(
         function ()
            local json = require("cjson")
            local tb = json.decode(whole)
            tb["data"][1]["t"] = "something apple 11"
            ngx.arg[1] = json.encode(tb)
         end
      )
      if not ok then
          ngx.arg[1] = errors
      end
   end
end
