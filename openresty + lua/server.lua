local host = "http://127.0.0.1:9090/diviner"
local jd = "http://diviner.jd.local"
local arg = ngx.req.get_uri_args()
if arg["p"] ~= "902008" then
    return host
else
    return jd
end
