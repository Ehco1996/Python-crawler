import requests
from parsel import Selector
import json
import time
from copyheaders import headers_raw_to_dict
import execjs
from requests_toolbelt.multipart.encoder import MultipartEncoder


class ZhihuClient(object):

    def __init__(self, username, passwd):
        self.s = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        self.post_headers_raw = b'''
            accept:application/json, text/plain, */*
            Accept-Encoding:gzip, deflate, br
            Accept-Language:zh-CN,zh;q=0.9,zh-TW;q=0.8
            authorization:oauth c3cef7c66a1843f8b3a9e6a1e3160e20
            Connection:keep-alive
            DNT:1
            Host:www.zhihu.com
            Origin:https://www.zhihu.com
            Referer:https://www.zhihu.com/signup?next=%2F
            User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
            '''
        self.username = username
        self.passwd = passwd

    def getHeaders(self):
        '''从网页源代码内解析出 uuid与Xsrftoken'''
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        z1 = self.s.get('https://www.zhihu.com/')
        sel = Selector(z1.text)
        jsdata = sel.css('div#data::attr(data-state)').extract_first()
        xudid = json.loads(jsdata)['token']['xUDID']
        xsrf = json.loads(jsdata)['token']['xsrf']
        headers = headers_raw_to_dict(self.post_headers_raw)
        headers['X-UDID'] = xudid
        headers['X-Xsrftoken'] = xsrf
        return headers

    def getdata(self, username, password, captcha=''):
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        timestamp = int(time.time()) * 1000
        js1 = execjs.compile("""
                function a(e, t, n) {
                    var r, o, a, i, c, s, u, l, y, b = 0,
                        g = [],
                        w = 0,
                        E = !1,
                        _ = [],
                        O = [],
                        C = !1,
                        T = !1;
                    if (n = n || {}, r = n.encoding || "UTF8", y = n.numRounds || 1, a = v(t, r), y !== parseInt(y, 10) || 1 > y) throw Error("numRounds must a integer >= 1");
                    if ("SHA-1" === e) c = 512, s = q, u = H, i = 160, l = function (e) {
                        return e.slice()
                    };
                    else if (0 === e.lastIndexOf("SHA-", 0))
                        if (s = function (t, n) {
                                return V(t, n, e)
                            }, u = function (t, n, r, o) {
                                var a, i;
                                if ("SHA-224" === e || "SHA-256" === e) a = 15 + (n + 65 >>> 9 << 4), i = 16;
                                else {
                                    if ("SHA-384" !== e && "SHA-512" !== e) throw Error("Unexpected error in SHA-2 implementation");
                                    a = 31 + (n + 129 >>> 10 << 5), i = 32
                                }
                                for (; t.length <= a;) t.push(0);
                                for (t[n >>> 5] |= 128 << 24 - n % 32, n += r, t[a] = 4294967295 & n, t[a - 1] = n / 4294967296 | 0, r = t.length, n = 0; n < r; n += i) o = V(t.slice(n, n + i), o, e);
                                if ("SHA-224" === e) t = [o[0], o[1], o[2], o[3], o[4], o[5], o[6]];
                                else if ("SHA-256" === e) t = o;
                                else if ("SHA-384" === e) t = [o[0].a, o[0].b, o[1].a, o[1].b, o[2].a, o[2].b, o[3].a, o[3].b, o[4].a, o[4].b, o[5].a, o[5].b];
                                else {
                                    if ("SHA-512" !== e) throw Error("Unexpected error in SHA-2 implementation");
                                    t = [o[0].a, o[0].b, o[1].a, o[1].b, o[2].a, o[2].b, o[3].a, o[3].b, o[4].a, o[4].b, o[5].a, o[5].b, o[6].a, o[6].b, o[7].a, o[7].b]
                                }
                                return t
                            }, l = function (e) {
                                return e.slice()
                            }, "SHA-224" === e) c = 512, i = 224;
                        else if ("SHA-256" === e) c = 512, i = 256;
                    else if ("SHA-384" === e) c = 1024, i = 384;
                    else {
                        if ("SHA-512" !== e) throw Error("Chosen SHA variant is not supported");
                        c = 1024, i = 512
                    } else {
                        if (0 !== e.lastIndexOf("SHA3-", 0) && 0 !== e.lastIndexOf("SHAKE", 0)) throw Error("Chosen SHA variant is not supported");
                        var S = 6;
                        if (s = G, l = function (e) {
                                var t, n = [];
                                for (t = 0; 5 > t; t += 1) n[t] = e[t].slice();
                                return n
                            }, "SHA3-224" === e) c = 1152, i = 224;
                        else if ("SHA3-256" === e) c = 1088, i = 256;
                        else if ("SHA3-384" === e) c = 832, i = 384;
                        else if ("SHA3-512" === e) c = 576, i = 512;
                        else if ("SHAKE128" === e) c = 1344, i = -1, S = 31, T = !0;
                        else {
                            if ("SHAKE256" !== e) throw Error("Chosen SHA variant is not supported");
                            c = 1088, i = -1, S = 31, T = !0
                        }
                        u = function (e, t, n, r, o) {
                            n = c;
                            var a, i = S,
                                s = [],
                                u = n >>> 5,
                                l = 0,
                                f = t >>> 5;
                            for (a = 0; a < f && t >= n; a += u) r = G(e.slice(a, a + u), r), t -= n;
                            for (e = e.slice(a), t %= n; e.length < u;) e.push(0);
                            for (a = t >>> 3, e[a >> 2] ^= i << 24 - a % 4 * 8, e[u - 1] ^= 128, r = G(e, r); 32 * s.length < o && (e = r[l % 5][l / 5 | 0], s.push((255 & e.b) << 24 | (65280 & e.b) << 8 | (16711680 & e.b) >> 8 | e.b >>> 24), !(32 * s.length >= o));) s.push((255 & e.a) << 24 | (65280 & e.a) << 8 | (16711680 & e.a) >> 8 | e.a >>> 24), 0 == 64 * (l += 1) % n && G(null, r);
                            return s
                        }
                    }
                    o = F(e), this.setHMACKey = function (t, n, a) {
                        var l;
                        if (!0 === E) throw Error("HMAC key already set");
                        if (!0 === C) throw Error("Cannot set HMAC key after calling update");
                        if (!0 === T) throw Error("SHAKE is not supported for HMAC");
                        if (r = (a || {}).encoding || "UTF8", n = v(n, r)(t), t = n.binLen, n = n.value, l = c >>> 3, a = l / 4 - 1, l < t / 8) {
                            for (n = u(n, t, 0, F(e), i); n.length <= a;) n.push(0);
                            n[a] &= 4294967040
                        } else if (l > t / 8) {
                            for (; n.length <= a;) n.push(0);
                            n[a] &= 4294967040
                        }
                        for (t = 0; t <= a; t += 1) _[t] = 909522486 ^ n[t], O[t] = 1549556828 ^ n[t];
                        o = s(_, o), b = c, E = !0
                    }, this.update = function (e) {
                        var t, n, r, i = 0,
                            u = c >>> 5;
                        for (t = a(e, g, w), e = t.binLen, n = t.value, t = e >>> 5, r = 0; r < t; r += u) i + c <= e && (o = s(n.slice(r, r + u), o), i += c);
                        b += i, g = n.slice(i >>> 5), w = e % c, C = !0
                    }, this.getHash = function (t, n) {
                        var r, a, c, s;
                        if (!0 === E) throw Error("Cannot call getHash after setting HMAC key");
                        if (c = m(n), !0 === T) {
                            if (-1 === c.shakeLen) throw Error("shakeLen must be specified in options");
                            i = c.shakeLen
                        }
                        switch (t) {
                            case "HEX":
                                r = function (e) {
                                    return f(e, i, c)
                                };
                                break;
                            case "B64":
                                r = function (e) {
                                    return p(e, i, c)
                                };
                                break;
                            case "BYTES":
                                r = function (e) {
                                    return d(e, i)
                                };
                                break;
                            case "ARRAYBUFFER":
                                try {
                                    a = new ArrayBuffer(0)
                                } catch (e) {
                                    throw Error("ARRAYBUFFER not supported by this environment")
                                }
                                r = function (e) {
                                    return h(e, i)
                                };
                                break;
                            default:
                                throw Error("format must be HEX, B64, BYTES, or ARRAYBUFFER")
                        }
                        for (s = u(g.slice(), w, b, l(o), i), a = 1; a < y; a += 1) !0 === T && 0 != i % 32 && (s[s.length - 1] &= 4294967040 << 24 - i % 32), s = u(s, i, 0, F(e), i);
                        return r(s)
                    }, this.getHMAC = function (t, n) {
                        var r, a, v, y;
                        if (!1 === E) throw Error("Cannot call getHMAC without first setting HMAC key");
                        switch (v = m(n), t) {
                            case "HEX":
                                r = function (e) {
                                    return f(e, i, v)
                                };
                                break;
                            case "B64":
                                r = function (e) {
                                    return p(e, i, v)
                                };
                                break;
                            case "BYTES":
                                r = function (e) {
                                    return d(e, i)
                                };
                                break;
                            case "ARRAYBUFFER":
                                try {
                                    r = new ArrayBuffer(0)
                                } catch (e) {
                                    throw Error("ARRAYBUFFER not supported by this environment")
                                }
                                r = function (e) {
                                    return h(e, i)
                                };
                                break;
                            default:
                                throw Error("outputFormat must be HEX, B64, BYTES, or ARRAYBUFFER")
                        }
                        return a = u(g.slice(), w, b, l(o), i), y = s(O, F(e)), y = u(a, i, c, y, i), r(y)
                    }
                }
                function i(e, t) {
                    this.a = e, this.b = t
                }
                function c(e, t, n) {
                    var r, o, a, i, c, s = e.length;
                    if (t = t || [0], n = n || 0, c = n >>> 3, 0 != s % 2) throw Error("String of HEX type must be in byte increments");
                    for (r = 0; r < s; r += 2) {
                        if (o = parseInt(e.substr(r, 2), 16), isNaN(o)) throw Error("String of HEX type contains invalid characters");
                        for (i = (r >>> 1) + c, a = i >>> 2; t.length <= a;) t.push(0);
                        t[a] |= o << 8 * (3 - i % 4)
                    }
                    return {
                        value: t,
                        binLen: 4 * s + n
                    }
                }
                function s(e, t, n) {
                    var r, o, a, i, c = [],
                        c = t || [0];
                    for (n = n || 0, o = n >>> 3, r = 0; r < e.length; r += 1) t = e.charCodeAt(r), i = r + o, a = i >>> 2, c.length <= a && c.push(0), c[a] |= t << 8 * (3 - i % 4);
                    return {
                        value: c,
                        binLen: 8 * e.length + n
                    }
                }
                function u(e, t, n) {
                    var r, o, a, i, c, s, u = [],
                        l = 0,
                        u = t || [0];
                    if (n = n || 0, t = n >>> 3, -1 === e.search(/^[a-zA-Z0-9=+\/]+$/)) throw Error("Invalid character in base-64 string");
                    if (o = e.indexOf("="), e = e.replace(/\=/g, ""), -1 !== o && o < e.length) throw Error("Invalid '=' found in base-64 string");
                    for (o = 0; o < e.length; o += 4) {
                        for (c = e.substr(o, 4), a = i = 0; a < c.length; a += 1) r = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".indexOf(c[a]), i |= r << 18 - 6 * a;
                        for (a = 0; a < c.length - 1; a += 1) {
                            for (s = l + t, r = s >>> 2; u.length <= r;) u.push(0);
                            u[r] |= (i >>> 16 - 8 * a & 255) << 8 * (3 - s % 4), l += 1
                        }
                    }
                    return {
                        value: u,
                        binLen: 8 * l + n
                    }
                }
                function l(e, t, n) {
                    var r, o, a, i = [],
                        i = t || [0];
                    for (n = n || 0, r = n >>> 3, t = 0; t < e.byteLength; t += 1) a = t + r, o = a >>> 2, i.length <= o && i.push(0), i[o] |= e[t] << 8 * (3 - a % 4);
                    return {
                        value: i,
                        binLen: 8 * e.byteLength + n
                    }
                }
                function f(e, t, n) {
                    var r = "";
                    t /= 8;
                    var o, a;
                    for (o = 0; o < t; o += 1) a = e[o >>> 2] >>> 8 * (3 - o % 4), r += "0123456789abcdef".charAt(a >>> 4 & 15) + "0123456789abcdef".charAt(15 & a);
                    return n.outputUpper ? r.toUpperCase() : r
                }
                function p(e, t, n) {
                    var r, o, a, i = "",
                        c = t / 8;
                    for (r = 0; r < c; r += 3)
                        for (o = r + 1 < c ? e[r + 1 >>> 2] : 0, a = r + 2 < c ? e[r + 2 >>> 2] : 0, a = (e[r >>> 2] >>> 8 * (3 - r % 4) & 255) << 16 | (o >>> 8 * (3 - (r + 1) % 4) & 255) << 8 | a >>> 8 * (3 - (r + 2) % 4) & 255, o = 0; 4 > o; o += 1) i += 8 * r + 6 * o <= t ? "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(a >>> 6 * (3 - o) & 63) : n.b64Pad;
                    return i
                }
                function d(e, t) {
                    var n, r, o = "",
                        a = t / 8;
                    for (n = 0; n < a; n += 1) r = e[n >>> 2] >>> 8 * (3 - n % 4) & 255, o += String.fromCharCode(r);
                    return o
                }
                function h(e, t) {
                    var n, r = t / 8,
                        o = new ArrayBuffer(r);
                    for (n = 0; n < r; n += 1) o[n] = e[n >>> 2] >>> 8 * (3 - n % 4) & 255;
                    return o
                }
                function m(e) {
                    var t = {
                        outputUpper: !1,
                        b64Pad: "=",
                        shakeLen: -1
                    };
                    if (e = e || {}, t.outputUpper = e.outputUpper || !1, !0 === e.hasOwnProperty("b64Pad") && (t.b64Pad = e.b64Pad), !0 === e.hasOwnProperty("shakeLen")) {
                        if (0 != e.shakeLen % 8) throw Error("shakeLen must be a multiple of 8");
                        t.shakeLen = e.shakeLen
                    }
                    if ("boolean" != typeof t.outputUpper) throw Error("Invalid outputUpper formatting option");
                    if ("string" != typeof t.b64Pad) throw Error("Invalid b64Pad formatting option");
                    return t
                }
                function v(e, t) {
                    var n;
                    switch (t) {
                        case "UTF8":
                        case "UTF16BE":
                        case "UTF16LE":
                            break;
                        default:
                            throw Error("encoding must be UTF8, UTF16BE, or UTF16LE")
                    }
                    switch (e) {
                        case "HEX":
                            n = c;
                            break;
                        case "TEXT":
                            n = function (e, n, r) {
                                var o, a, i, c, s, u = [],
                                    l = [],
                                    f = 0,
                                    u = n || [0];
                                if (n = r || 0, i = n >>> 3, "UTF8" === t)
                                    for (o = 0; o < e.length; o += 1)
                                        for (r = e.charCodeAt(o), l = [], 128 > r ? l.push(r) : 2048 > r ? (l.push(192 | r >>> 6), l.push(128 | 63 & r)) : 55296 > r || 57344 <= r ? l.push(224 | r >>> 12, 128 | r >>> 6 & 63, 128 | 63 & r) : (o += 1, r = 65536 + ((1023 & r) << 10 | 1023 & e.charCodeAt(o)), l.push(240 | r >>> 18, 128 | r >>> 12 & 63, 128 | r >>> 6 & 63, 128 | 63 & r)), a = 0; a < l.length; a += 1) {
                                            for (s = f + i, c = s >>> 2; u.length <= c;) u.push(0);
                                            u[c] |= l[a] << 8 * (3 - s % 4), f += 1
                                        } else if ("UTF16BE" === t || "UTF16LE" === t)
                                            for (o = 0; o < e.length; o += 1) {
                                                for (r = e.charCodeAt(o), "UTF16LE" === t && (a = 255 & r, r = a << 8 | r >>> 8), s = f + i, c = s >>> 2; u.length <= c;) u.push(0);
                                                u[c] |= r << 8 * (2 - s % 4), f += 2
                                            }
                                return {
                                    value: u,
                                    binLen: 8 * f + n
                                }
                            };
                            break;
                        case "B64":
                            n = u;
                            break;
                        case "BYTES":
                            n = s;
                            break;
                        case "ARRAYBUFFER":
                            try {
                                n = new ArrayBuffer(0)
                            } catch (e) {
                                throw Error("ARRAYBUFFER not supported by this environment")
                            }
                            n = l;
                            break;
                        default:
                            throw Error("format must be HEX, TEXT, B64, BYTES, or ARRAYBUFFER")
                    }
                    return n
                }
                function y(e, t) {
                    return e << t | e >>> 32 - t
                }
                function b(e, t) {
                    return 32 < t ? (t -= 32, new i(e.b << t | e.a >>> 32 - t, e.a << t | e.b >>> 32 - t)) : 0 !== t ? new i(e.a << t | e.b >>> 32 - t, e.b << t | e.a >>> 32 - t) : e
                }
                function g(e, t) {
                    return e >>> t | e << 32 - t
                }
                function w(e, t) {
                    var n = null,
                        n = new i(e.a, e.b);
                    return n = 32 >= t ? new i(n.a >>> t | n.b << 32 - t & 4294967295, n.b >>> t | n.a << 32 - t & 4294967295) : new i(n.b >>> t - 32 | n.a << 64 - t & 4294967295, n.a >>> t - 32 | n.b << 64 - t & 4294967295)
                }
                function E(e, t) {
                    return 32 >= t ? new i(e.a >>> t, e.b >>> t | e.a << 32 - t & 4294967295) : new i(0, e.a >>> t - 32)
                }
                function _(e, t, n) {
                    return e & t ^ ~e & n
                }
                function O(e, t, n) {
                    return new i(e.a & t.a ^ ~e.a & n.a, e.b & t.b ^ ~e.b & n.b)
                }
                function C(e, t, n) {
                    return e & t ^ e & n ^ t & n
                }
                function T(e, t, n) {
                    return new i(e.a & t.a ^ e.a & n.a ^ t.a & n.a, e.b & t.b ^ e.b & n.b ^ t.b & n.b)
                }
                function S(e) {
                    return g(e, 2) ^ g(e, 13) ^ g(e, 22)
                }
                function k(e) {
                    var t = w(e, 28),
                        n = w(e, 34);
                    return e = w(e, 39), new i(t.a ^ n.a ^ e.a, t.b ^ n.b ^ e.b)
                }
                function j(e) {
                    return g(e, 6) ^ g(e, 11) ^ g(e, 25)
                }
                function P(e) {
                    var t = w(e, 14),
                        n = w(e, 18);
                    return e = w(e, 41), new i(t.a ^ n.a ^ e.a, t.b ^ n.b ^ e.b)
                }
                function A(e) {
                    return g(e, 7) ^ g(e, 18) ^ e >>> 3
                }
                function x(e) {
                    var t = w(e, 1),
                        n = w(e, 8);
                    return e = E(e, 7), new i(t.a ^ n.a ^ e.a, t.b ^ n.b ^ e.b)
                }
                function I(e) {
                    return g(e, 17) ^ g(e, 19) ^ e >>> 10
                }
                function N(e) {
                    var t = w(e, 19),
                        n = w(e, 61);
                    return e = E(e, 6), new i(t.a ^ n.a ^ e.a, t.b ^ n.b ^ e.b)
                }
                function R(e, t) {
                    var n = (65535 & e) + (65535 & t);
                    return ((e >>> 16) + (t >>> 16) + (n >>> 16) & 65535) << 16 | 65535 & n
                }
                function M(e, t, n, r) {
                    var o = (65535 & e) + (65535 & t) + (65535 & n) + (65535 & r);
                    return ((e >>> 16) + (t >>> 16) + (n >>> 16) + (r >>> 16) + (o >>> 16) & 65535) << 16 | 65535 & o
                }
                function D(e, t, n, r, o) {
                    var a = (65535 & e) + (65535 & t) + (65535 & n) + (65535 & r) + (65535 & o);
                    return ((e >>> 16) + (t >>> 16) + (n >>> 16) + (r >>> 16) + (o >>> 16) + (a >>> 16) & 65535) << 16 | 65535 & a
                }
                function L(e, t) {
                    var n, r, o;
                    return n = (65535 & e.b) + (65535 & t.b), r = (e.b >>> 16) + (t.b >>> 16) + (n >>> 16), o = (65535 & r) << 16 | 65535 & n, n = (65535 & e.a) + (65535 & t.a) + (r >>> 16), r = (e.a >>> 16) + (t.a >>> 16) + (n >>> 16), new i((65535 & r) << 16 | 65535 & n, o)
                }
                function z(e, t, n, r) {
                    var o, a, c;
                    return o = (65535 & e.b) + (65535 & t.b) + (65535 & n.b) + (65535 & r.b), a = (e.b >>> 16) + (t.b >>> 16) + (n.b >>> 16) + (r.b >>> 16) + (o >>> 16), c = (65535 & a) << 16 | 65535 & o, o = (65535 & e.a) + (65535 & t.a) + (65535 & n.a) + (65535 & r.a) + (a >>> 16), a = (e.a >>> 16) + (t.a >>> 16) + (n.a >>> 16) + (r.a >>> 16) + (o >>> 16), new i((65535 & a) << 16 | 65535 & o, c)
                }
                function U(e, t, n, r, o) {
                    var a, c, s;
                    return a = (65535 & e.b) + (65535 & t.b) + (65535 & n.b) + (65535 & r.b) + (65535 & o.b), c = (e.b >>> 16) + (t.b >>> 16) + (n.b >>> 16) + (r.b >>> 16) + (o.b >>> 16) + (a >>> 16), s = (65535 & c) << 16 | 65535 & a, a = (65535 & e.a) + (65535 & t.a) + (65535 & n.a) + (65535 & r.a) + (65535 & o.a) + (c >>> 16), c = (e.a >>> 16) + (t.a >>> 16) + (n.a >>> 16) + (r.a >>> 16) + (o.a >>> 16) + (a >>> 16), new i((65535 & c) << 16 | 65535 & a, s)
                }
                function B(e) {
                    var t, n = 0,
                        r = 0;
                    for (t = 0; t < arguments.length; t += 1) n ^= arguments[t].b, r ^= arguments[t].a;
                    return new i(r, n)
                }
                function F(e) {
                    var t, n = [];
                    if ("SHA-1" === e) n = [1732584193, 4023233417, 2562383102, 271733878, 3285377520];
                    else if (0 === e.lastIndexOf("SHA-", 0)) switch (n = [3238371032, 914150663, 812702999, 4144912697, 4290775857, 1750603025, 1694076839, 3204075428], t = [1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225], e) {
                        case "SHA-224":
                            break;
                        case "SHA-256":
                            n = t;
                            break;
                        case "SHA-384":
                            n = [new i(3418070365, n[0]), new i(1654270250, n[1]), new i(2438529370, n[2]), new i(355462360, n[3]), new i(1731405415, n[4]), new i(41048885895, n[5]), new i(3675008525, n[6]), new i(1203062813, n[7])];
                            break;
                        case "SHA-512":
                            n = [new i(t[0], 4089235720), new i(t[1], 2227873595), new i(t[2], 4271175723), new i(t[3], 1595750129), new i(t[4], 2917565137), new i(t[5], 725511199), new i(t[6], 4215389547), new i(t[7], 327033209)];
                            break;
                        default:
                            throw Error("Unknown SHA variant")
                    } else {
                        if (0 !== e.lastIndexOf("SHA3-", 0) && 0 !== e.lastIndexOf("SHAKE", 0)) throw Error("No SHA variants supported");
                        for (e = 0; 5 > e; e += 1) n[e] = [new i(0, 0), new i(0, 0), new i(0, 0), new i(0, 0), new i(0, 0)]
                    }
                    return n
                }
                function q(e, t) {
                    var n, r, o, a, i, c, s, u = [];
                    for (n = t[0], r = t[1], o = t[2], a = t[3], i = t[4], s = 0; 80 > s; s += 1) u[s] = 16 > s ? e[s] : y(u[s - 3] ^ u[s - 8] ^ u[s - 14] ^ u[s - 16], 1), c = 20 > s ? D(y(n, 5), r & o ^ ~r & a, i, 1518500249, u[s]) : 40 > s ? D(y(n, 5), r ^ o ^ a, i, 1859775393, u[s]) : 60 > s ? D(y(n, 5), C(r, o, a), i, 2400959708, u[s]) : D(y(n, 5), r ^ o ^ a, i, 3395469782, u[s]), i = a, a = o, o = y(r, 30), r = n, n = c;
                    return t[0] = R(n, t[0]), t[1] = R(r, t[1]), t[2] = R(o, t[2]), t[3] = R(a, t[3]), t[4] = R(i, t[4]), t
                }
                function H(e, t, n, r) {
                    var o;
                    for (o = 15 + (t + 65 >>> 9 << 4); e.length <= o;) e.push(0);
                    for (e[t >>> 5] |= 128 << 24 - t % 32, t += n, e[o] = 4294967295 & t, e[o - 1] = t / 4294967296 | 0, t = e.length, o = 0; o < t; o += 16) r = q(e.slice(o, o + 16), r);
                    return r
                }
                function V(e, t, n) {
                    var r, o, a, c, s, u, l, f, p, d, h, m, v, y, b, g, w, E, B, F, q, H, V, G = [];
                    if ("SHA-224" === n || "SHA-256" === n) d = 64, m = 1, H = Number, v = R, y = M, b = D, g = A, w = I, E = S, B = j, q = C, F = _, V = W;
                    else {
                        if ("SHA-384" !== n && "SHA-512" !== n) throw Error("Unexpected error in SHA-2 implementation");
                        d = 80, m = 2, H = i, v = L, y = z, b = U, g = x, w = N, E = k, B = P, q = T, F = O, V = K
                    }
                    for (n = t[0], r = t[1], o = t[2], a = t[3], c = t[4], s = t[5], u = t[6], l = t[7], h = 0; h < d; h += 1) 16 > h ? (p = h * m, f = e.length <= p ? 0 : e[p], p = e.length <= p + 1 ? 0 : e[p + 1], G[h] = new H(f, p)) : G[h] = y(w(G[h - 2]), G[h - 7], g(G[h - 15]), G[h - 16]), f = b(l, B(c), F(c, s, u), V[h], G[h]), p = v(E(n), q(n, r, o)), l = u, u = s, s = c, c = v(a, f), a = o, o = r, r = n, n = v(f, p);
                    return t[0] = v(n, t[0]), t[1] = v(r, t[1]), t[2] = v(o, t[2]), t[3] = v(a, t[3]), t[4] = v(c, t[4]), t[5] = v(s, t[5]), t[6] = v(u, t[6]), t[7] = v(l, t[7]), t
                }
                function G(e, t) {
                    var n, r, o, a, c = [],
                        s = [];
                    if (null !== e)
                        for (r = 0; r < e.length; r += 2) t[(r >>> 1) % 5][(r >>> 1) / 5 | 0] = B(t[(r >>> 1) % 5][(r >>> 1) / 5 | 0], new i((255 & e[r + 1]) << 24 | (65280 & e[r + 1]) << 8 | (16711680 & e[r + 1]) >>> 8 | e[r + 1] >>> 24, (255 & e[r]) << 24 | (65280 & e[r]) << 8 | (16711680 & e[r]) >>> 8 | e[r] >>> 24));
                    for (n = 0; 24 > n; n += 1) {
                        for (a = F("SHA3-"), r = 0; 5 > r; r += 1) c[r] = B(t[r][0], t[r][1], t[r][2], t[r][3], t[r][4]);
                        for (r = 0; 5 > r; r += 1) s[r] = B(c[(r + 4) % 5], b(c[(r + 1) % 5], 1));
                        for (r = 0; 5 > r; r += 1)
                            for (o = 0; 5 > o; o += 1) t[r][o] = B(t[r][o], s[r]);
                        for (r = 0; 5 > r; r += 1)
                            for (o = 0; 5 > o; o += 1) a[o][(2 * r + 3 * o) % 5] = b(t[r][o], Q[r][o]);
                        for (r = 0; 5 > r; r += 1)
                            for (o = 0; 5 > o; o += 1) t[r][o] = B(a[r][o], new i(~a[(r + 1) % 5][o].a & a[(r + 2) % 5][o].a, ~a[(r + 1) % 5][o].b & a[(r + 2) % 5][o].b));
                        t[0][0] = B(t[0][0], Y[n])
                    }
                    return t
                }
                function run(e,n){
                    // e = password,
                    // n 为时间戳，如1515735045595
                    //client_id,现在默认为 c3cef7c66a1843f8b3a9e6a1e3160e20
                    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20';
                    r = new a("SHA-1", "TEXT");
                    r.setHMACKey("d1b964811afb40118a12068ff74a12f4", "TEXT");
                    r.update(e);
                    r.update(client_id);
                    r.update("com.zhihu.web");
                    r.update(String(n));
                    return r.getHMAC("HEX")
                }
        """)
        signature = js1.call('run', 'password', timestamp)
        data = {
            'client_id': client_id, 'grant_type': 'password',
            'timestamp': str(timestamp), 'source': 'com.zhihu.web',
            'signature': signature, 'username': username,
            'password': password, 'captcha': captcha,
            'lang': 'en', 'ref_source': 'homepage', 'utm_source': ''
        }
        return data

    def checkcapthca(self, headers, cn=True):
        '检查是否需要验证码,无论需不需要，必须要发一个请求'
        if cn:
            url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        else:
            url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        headers.pop('X-Xsrftoken')
        z = self.s.get(url, headers=headers)
        print(z.json())
        return z.json()

    def login(self, username, password):
        url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        headers = self.getHeaders()
        data = self.getdata(username, password)
        self.checkcapthca(headers)
        # multipart_encoder = MultipartEncoder(fieles=data, boundary='----WebKitFormBoundarycGPN1xiTi2hCSKKZ')
        # todo:boundary后面的几位数可以随机，现在是固定的
        encoder = MultipartEncoder(
            data, boundary='----WebKitFormBoundarycGPN1xiTi2hCSKKZ')
        headers['Content-Type'] = encoder.content_type
        z2 = self.s.post(url, headers=headers, data=encoder.to_string(), )
        print(z2.json())
        print('尝试登录完毕')

    def get_session(self):
        '''
        返回登录后的session
        '''
        self.login(self.username, self.passwd)
        return self.s


