local file,err = io.open("/home/admin/lixiaomei/test.txt", "r")
if file == nil then
   ngx.arg[1] = err
else
   local temp = file:read()
   file:close()
   ngx.arg[1] = temp
   ngx.arg[2] = true
end
