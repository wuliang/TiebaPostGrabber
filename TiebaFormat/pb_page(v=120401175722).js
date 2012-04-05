var Page = {
        toQuerystring: function (a) {
            var c = "";
            for (var b in a) {
                c += b + "=" + a[b] + "&"
            }
            return c.substr(0, c.length - 1)
        },
        isBaiduDomain: function (b) {
            var a = /^((https:\/\/|http:\/\/|ftp:\/\/|rtsp:\/\/|mms:\/\/)(([0-9a-zA-Z\.\-\_]+\.baidu.com)|(baidu.com))\/)/;
            return a.test(b)
        },
        resizePic: function (d, a, i, e) {
            var h = a || 120;
            var f = i || 120;
            var c = false;
            var g = new Image();
            g.src = d.src;
            var b = Page.getRightWH(g.width, g.height, h, f);
            d.style.width = b[0] + "px";
            d.style.height = b[1] + "px";
            d.style.visibility = "visible";
            if (e == true) {
                d.style.marginTop = (i - parseInt(b[1])) / 2 + "px"
            }
            g = null;
            return c
        },
        getRightWH: function (a, d, b, f) {
            var c = 0,
                e = a,
                g = d;
            if (a > b) {
                c += 1
            }
            if (d > f) {
                c += 2
            }
            switch (c) {
            case 1:
                e = b;
                e = d * b / a;
            case 2:
                g = f;
                e = a * f / d;
            case 3:
                g = (d / f > a / b) ? f : d * b / a;
                e = (d / f > a / b) ? a * f / d : b
            }
            if (c != 0) {
                need_resize = true
            }
            return [e, g]
        },
        resizcImg: function (g, c) {
            var f = c;
            var h = false;
            var d = g;
            if (d.width == 0) {
                var e = this;
                var a = arguments;
                setTimeout(function () {
                    a.callee.apply(e, a)
                }, 100);
                return false
            }
            if (d.width > c) {
                h = true
            }
            var b = Page.getImgRightWH(d.width, d.height, c);
            g.style.width = b[0] + "px";
            g.style.height = b[1] + "px";
            g.style.visibility = "visible";
            return h
        },
        getImgRightWH: function (a, c, b) {
            var d = a,
                e = c;
            if (a > b) {
                d = b;
                e = c * b / a
            }
            d = parseInt(d);
            e = parseInt(e);
            return [d, e]
        },
        resetChangedSizeImage: function (b, a) {
            if (b && a && b == "old") {
                if (Page.resizcImg(a, 570)) {
                    var c = a;
                    if (Page.isBaiduDomain(c.src)) {
                        c.style.cursor = "pointer";
                        c.title = "点击查看原图";
                        c.onclick = function (f) {
                            if (!f) {
                                f = window.event
                            }
                            var d = f.target || f.srcElement;
                            if (NsLogLinker.isOutLink(d.src)) {
                                NsLogLinker.stat(d.src, 110)
                            }
                            window.open(d.src, "_blank")
                        }
                    }
                }
                return true
            }
        },
        bindOpenImg: function () {
            var d = document.getElementsByTagName("IMG");
            for (var a = 0, c = d.length; a < c; a++) {
                var b = d[a];
                if (b && b.className == "BDE_Image" && b.getAttribute("changedsize") == "true") {
                    if (Page.isBaiduDomain(b.src)) {
                        b.style.cursor = "pointer";
                        b.title = "点击查看原图";
                        b.onclick = function (g) {
                            if (!g) {
                                g = window.event
                            }
                            var f = g.target || g.srcElement;
                            if (NsLogLinker.isOutLink(f.src)) {
                                NsLogLinker.stat(f.src, 110)
                            }
                            window.open(f.src, "_blank")
                        }
                    }
                }
            }
        },
        changeNumber: function (g, f) {
            var a = PageData.curr_page_num;
            var d = PageData.all_page_num;
            if (f.tagName != "input" && f.tagName != "INPUT" && a > 0 && a <= d) {
                var c = 0;
                var b = PageData.thread_cur_url;
                var e = /&pn=[^&]+/;
                if (e.exec(b)) {
                    b = RegExp.leftContext + RegExp.rightContext
                }
                c = (a - 1 + g) * 30;
                if (c >= 0 && c <= (d - 1) * 30) {
                    window.location.href = b + "&pn=" + c
                }
                return true
            }
            return false
        },
        changeVersion: function (b) {
            var a = PageData.thread_cur_url;
            var c = /&rs1=[^&]+/;
            if (c.exec(a)) {
                a = RegExp.leftContext + RegExp.rightContext
            }
            window.location.href = a + "&rs1=" + b
        },
        changeVersionPhp: function (b) {
            var a = PageData.thread_cur_url;
            var c = /&v=[^&]+/;
            if (c.exec(a)) {
                a = RegExp.leftContext + RegExp.rightContext
            }
            window.location.href = a + "&v=" + b
        },
        init: function () {
            Page.resetChangedSizeImage()
        },
        checkErrorImage: function (b) {
            var a = b.parentNode;
            a.innerHTML = "<br><img src='http://yourimgloaderroratbaidu' border='0'/>"
        },
        sign_change_img: function (a) {
            a.src = TbConf.domain.TB_STATIC + "tb/static-itieba/img/sign_err.png";
            a.width = 100;
            a.height = 25
        },
        login: function () {
            TbCom.process("User", "buildLoginFrame")
        },
        isString: function (a) {
            return typeof a === "string"
        },
        escapeHTML: function (a) {
            if (Page.isString(a)) {
                return a.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;")
            } else {
                return a
            }
        },
        getByteLength: function (a) {
            return a.replace(/[^\x00-\xff]/g, "mm").length
        },
        subByteFix: function (e, f, d) {
            if (Page.getByteLength(e) <= f) {
                return e
            }
            for (var b = Math.floor((f - 2) / 2), a = e.length; b < a; b++) {
                var c = e.substring(0, b);
                if (Page.getByteLength(c) >= f) {
                    return c + (d ? d : "")
                }
            }
            return e
        }
    };
Page.Date = {};
Page.Date.lang = {};
Page.Date.lang.dayNames = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
Page.Date.lang.abbreviatedDayNames = ["日", "一", "二", "三", "四", "五", "六"];
Page.Date.lang.shortestDayNames = ["日", "一", "二", "三", "四", "五", "六"];
Page.Date.lang.firstLetterDayNames = ["日", "一", "二", "三", "四", "五", "六"];
Page.Date.format = function (b, d) {
    var a = b;
    var c = function (e) {
            return e < 10 ? "0" + e : e
        };
    return d.replace(/dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?/g, function (e) {
        switch (e) {
        case "hh":
            return c(a.getHours() < 13 ? (a.getHours() === 0 ? 12 : a.getHours()) : (a.getHours() - 12));
        case "h":
            return a.getHours() < 13 ? (a.getHours() === 0 ? 12 : a.getHours()) : (a.getHours() - 12);
        case "HH":
            return c(a.getHours());
        case "H":
            return a.getHours();
        case "mm":
            return c(a.getMinutes());
        case "m":
            return a.getMinutes();
        case "ss":
            return c(a.getSeconds());
        case "s":
            return a.getSeconds();
        case "yyyy":
            var f = "000" + a.getFullYear();
            return f.substring(f.length - 4);
        case "yy":
            return a.toString("yyyy").substring(2);
        case "dddd":
            return Page.Date.lang.dayNames[a.getDay()];
        case "ddd":
            return Page.Date.lang.abbreviatedDayNames[a.getDay()];
        case "dd":
            return c(a.getDate());
        case "d":
            return a.getDate().toString();
        case "MM":
            return c((a.getMonth() + 1));
        case "M":
            return a.getMonth() + 1
        }
    })
};
var FlashBuilder = {
        buildEmbed: function (c, a) {
            var b = this.getEmbedHtml(a);
            if (typeof c != "undefined") {
                document.getElementById(c).innerHTML = b
            }
        },
        buildObjAndEmbed: function (c, a) {
            var b = this.getObjAndEmbedHtml(a);
            if (typeof c != "undefined") {
                document.body.append(b)
            } else {
                document.getElementById(c).innerHTML = b
            }
        },
        getEmbedHtml: function (a) {
            var b = '<embed id="' + (a.id || "") + '" class="' + (a.className || "") + '" pluginspage="http://www.macromedia.com/go/getflashplayer"';
            b += ' src="' + a.src + '"';
            b += ' flashvars="' + a.flashvars + '"';
            b += ' width="' + (a.width || 550) + '" height="' + (a.height || 480) + '"';
            b += ' type="application/x-shockwave-flash" wmode="transparent" play="true" loop="false" ';
            b += ' menu="false" allowscriptaccess="' + (a.allowscriptaccess || "always") + '" scale="noborder">';
            return b
        },
        getObjAndEmbedHtml: function (a) {
            var b = '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"';
            b += ' codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9.0.0" ';
            b += 'WIDTH="' + (a.width || 550) + '" HEIGHT="' + (a.height || 480) + '" id="voteFlash">';
            b += '<PARAM NAME=movie VALUE="' + a.src + '">';
            b += "<PARAM NAME=quality VALUE=high>";
            b += '<PARAM NAME=flashvars VALUE="' + a.flashvars + '">';
            b += "<PARAM NAME=allowScriptAccess VALUE=" + (a.allowscriptaccess || "always") + ">";
            b += this.getEmbedHtml(a);
            b += "</object>";
            return b
        }
    };
