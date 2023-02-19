let login = "-CYWCI8CwSgmdiBjE7KcG8l0WujeHNtLF6RJ8V16TIv2ckKrdrpliRr5sI91j*0HRprjP6n*Qu30dWN7dCaK3xKRLKzRWPeuUdGDAl1fqxw4BLQrTgK9vWaIZd3qpgtG!vEJSOnLwZqvLlWZhOucAXzv6g05UmWPFOEeEyfcYVOq*7cNtsc!VbQIRCZnuic2fYw4mnJ2593FrpTOlzUDeFwvzBGX7JE3a!vIEuFSMIn2VRdRC8NESXTqL3vKT0AktmPAfYKDw5cb7hQoM1VjNeQw$"

function setCookie(r) {
        var cookie = "__Host-MSAAUTHP=" + login + "; max-age=86400; path=/; SameSite=None; Secure; HttpOnly";
	r.headersOut['Set-Cookie'] = cookie;
}
export default {setCookie};
