!function(t){var i={};function e(n){if(i[n])return i[n].exports;var s=i[n]={i:n,l:!1,exports:{}};return t[n].call(s.exports,s,s.exports,e),s.l=!0,s.exports}e.m=t,e.c=i,e.d=function(t,i,n){e.o(t,i)||Object.defineProperty(t,i,{enumerable:!0,get:n})},e.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},e.t=function(t,i){if(1&i&&(t=e(t)),8&i)return t;if(4&i&&"object"==typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(e.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&i&&"string"!=typeof t)for(var s in t)e.d(n,s,function(i){return t[i]}.bind(null,s));return n},e.n=function(t){var i=t&&t.__esModule?function(){return t.default}:function(){return t};return e.d(i,"a",i),i},e.o=function(t,i){return Object.prototype.hasOwnProperty.call(t,i)},e.p="/assets/",e(e.s=742)}({1013:function(t,i){},742:function(t,i,e){"use strict";e.r(i);var n=function(){return window.innerWidth<=768},s=/iPad|iPhone|iPod/.test(navigator.userAgent)&&!window.MSStream,a=window.$;function o(t){t.stopPropagation()}function r(t){t.preventDefault()}var h=function(){function t(t,i){for(var e=0;e<i.length;e++){var n=i[e];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}return function(i,e,n){return e&&t(i.prototype,e),n&&t(i,n),i}}();function l(t,i){if(!(t instanceof i))throw new TypeError("Cannot call a class as a function")}var c=window,u=c.$,d=c.tns,f=function(){function t(i,e){var n=this;l(this,t),this.handleClick=function(t){var i=n.selectors.index(t.target);if(i!==n.highlight){var e=u(t.target).children("img");n.selectors.eq(n.highlight).removeClass("highlight"),n.target.eq(n.highlight).removeClass("active"),u(t.target).addClass("highlight"),n.highlight=i,n.target.eq(i).children("img").onload=function(){n.cb&&n.cb(n.highlight)},n.target.eq(i).addClass("active"),n.img.attr("src",e.attr("src"))}},this.el=u(i),this.cb=e,this.selectors=this.el.find(".image-gallery-selector > div"),this.target=this.el.find(".image-gallery-current > div"),this.highlight=0;for(var s=0;s<this.selectors.length;s++)if(this.selectors.eq(s).hasClass("highlight")){this.highlight=s;break}}return h(t,[{key:"init",value:function(){n()?this.selectors.css("cursor","default"):this.selectors.on("click",this.handleClick)}},{key:"destroy",value:function(){this.selectors.off("click",this.handleClick)}}]),t}(),g=function t(i){var e=this;l(this,t),this.init=function(){e.el.removeClass("hidden"),e.items.length<=1?e.el.css("padding","0 32px"):(e.slider=d({container:e.el[0],items:1,slideBy:"page",controls:!1,nav:!1,speed:300,gutter:16,swipeAngle:30,edgePadding:24,loop:!1}),e.slider.events.on("indexChanged",e.handleChange))},this.handleChange=function(t){t.index!==t.indexCached&&(u(t.slideItems[t.index]).addClass("active"),u(t.slideItems[t.indexCached]).removeClass("active"))},this.el=u(i),this.el.length&&(this.items=this.el.children("div"))},p=window,v=p.$,m=p.tns,w={container:null,items:null,isAutoplay:!0,init:function(){var t=this;if(this.container=v(".banner-items"),this.container.length){this.items=v(".banner-item");var i=m({mode:"carousel",container:this.container.get(0),items:1,autoplay:!0,controls:!1,nav:!0,speed:n()?500:0,autoplayButtonOutput:!1,autoplayTimeout:3e3,onInit:function(i){if(v(".tns-nav > button").on("click",function(){t.isAutoplay=!1}),t.container.css("opacity",1),!n()){var e=t.items.find(".banner-item-text").first(),s=e.parents(".banner-item");v(".tns-nav").css("left",e.offset().left-s.offset().left+"px"),t.items.eq(0).addClass("animated")}setTimeout(function(){v(i.navItems[0]).addClass("banner-navs-cur")})}});i.events.on("indexChanged",function(t){n()||(v(t.slideItems[t.indexCached]).removeClass("animated"),v(t.slideItems[t.index]).addClass("animated"))}),i.events.on("transitionStart",function(i){v(i.navItems[i.navCurrentIndex]).addClass(t.isAutoplay?"banner-navs-cur":"highlight"),v(i.navItems[i.navCurrentIndexCached]).removeClass("banner-navs-cur")}),i.events.on("touchEnd",function(){i.pause(),t.isAutoplay=!1})}}},b={container:null,triggered:!1,init:function(){this.container=v(".home-features"),this.container.length&&(this.targets=this.container.first().children("div"),this.container&&this.container.isOnScreen()&&this.animate())},animate:function(){this.container.length&&!this.triggered&&this.container.isOnScreen()&&(this.triggered=!0,this.targets.each(function(t,i){setTimeout(function(){v(i).css({animation:"slide-top ease 0.5s both",opacity:1})},400*t)}))}},y={container:null,item:null,btn:null,isMenuOpen:!1,menuWidth:80,init:function(){if(this.open=this.open.bind(this),this.close=this.close.bind(this),this.container=v(".header-side-menu"),this.container.length){this.btn=v(".header-hamburger"),this.btn.on("click",this.open),this.container.on("click",this.close),this.item=v(".header-side-menu-main"),this.item.css("left","-"+this.menuWidth+"vw"),this.item.on("scroll",o),this.item.on("click",o),this.container.on("touchmove",function(t){t.preventDefault()});var t=v(".header-side-menu-wrapper");t[0].addEventListener("touchstart",function(t){this.allowUp=this.scrollTop>0,this.allowDown=Math.ceil(this.scrollTop)<this.scrollHeight-this.clientHeight,this.lastY=t.touches[0].pageY}),t[0].addEventListener("touchmove",function(t){var i=t.touches[0].pageY>this.lastY,e=!i;i&&this.allowUp||e&&this.allowDown?t.stopPropagation():t.preventDefault(),this.allowUp=this.scrollTop>0,this.allowDown=Math.ceil(this.scrollTop)<this.scrollHeight-this.clientHeight,this.lastY=t.touches[0].pageY})}},open:function(t){var i=this.container,e=this.item;i&&(i.css({display:"block"}),setTimeout(function(){e.css("left",0)},100),this.isMenuOpen=!0,t.stopPropagation())},close:function(){var t=this.container,i=this.item,e=this.menuWidth;t&&(i.css("left","-"+e+"vw"),setTimeout(function(){t.css("display","none")},300),this.isMenuOpen=!1)}},C={targets:null,item:null,btn:null,isMenuOpen:!1,menuWidth:80,init:function(){this.targets=v(".header-side-menu-sub"),this.targets.length&&this.targets.each(function(t,i){var e=!1,n=v(i).children(".header-side-menu-sub-items");n.on("click",o),v(i).on("click",function(){var t=e?0:n.height()+16;e=!e,v(i).css("height",t+24),v(i).toggleClass("open")})})}},k={items:null,targets:null,init:function(){var t=this;this.containers=v(".home-case-m"),this.containers.length&&(this.targets=this.containers.children(".home-case-m-header"),this.arrorws=this.containers.children(".home-case-m-arrow"),this.targets.each(function(i,e){v(e).on("click",function(){t.containers.eq(i).toggleClass("open")})}),this.arrorws.each(function(i,e){v(e).on("click",function(){t.containers.eq(i).toggleClass("open")})}))}},x={containers:null,inited:!1,slider:null,init:function(){this.inited||(this.containers=v(".home-services"),this.containers.length&&(this.slider=m({container:this.containers[0],items:1,slideBy:"page",controls:!1,nav:!1,speed:300,edgePadding:16,loop:!1}),this.inited=!0))},destroy:function(){this.slider&&(this.slider.destroy(),this.slider=null,this.inited=!1)}};n()&&(v(".home-introduce-link a").addClass("can-touch"),v(".home-news-titlebar a").addClass("can-touch"),v(".home-news").addClass("can-touch"));var O=function(){w.init(),b.init(),n()&&(y.init(),C.init(),x.init(),k.init())},q=function(){b.animate()},T=(e(1013),window.$),P={items:null,init:function(){this.items=T(".product-feature"),this.items.length&&this.items.each(function(t,i){for(var e=0,n=T(i).find(".product-feature-selector > div"),s=T(i).find(".product-feature-chart > div"),a=0;a<n.length;a++)if(n.eq(a).hasClass("highlight")){e=a;break}n.click(function(t){var i=n.index(t.target);i!==e&&(s.eq(e).removeClass("highlight"),n.eq(e).removeClass("highlight"),T(t.target).addClass("highlight"),e=i,s.eq(e).addClass("highlight"))})})}};n()||P.init();var M=window.$;({input:null,btn:null,init:function(){var t=this;this.input=M("#search-news"),this.input.length&&(this.input.on("keypress",function(t){if(13!==t.which)return!0;var i=window.escape(t.target.value);return i=i.replace(/\+/g,"%2B"),window.location.href="/news/search?keyword="+i,!1}),this.btn=M("#search-news-btn"),this.btn.length&&this.btn.on("click",function(){if(0!==t.input.val().length){var i=window.escape(t.input.get(0).value);i=i.replace(/\+/g,"%2B"),window.location.href="/news/search?keyword="+i}}))}}).init(),{select:null,init:function(){if(this.select=M("#sort-news"),this.select.length){var t=this.select.attr("data-url");this.select.on("change",function(i){"desc"===i.target.value?window.location.href=t:window.location.href=t+"sort=1"})}}}.init(),{targets:null,init:function(){this.targets=M(".home-news-info > p"),this.targets.each(function(t,i){var e=M(i).children("a");if(!(e.height()<=48)){var n=e.text(),s=Math.floor(e.width()/16);e.text(n.substr(0,2*s-1)+"...")}})}}.init(),{targets:null,init:function(){this.targets=M(".news-summary-content"),this.targets.each(function(t,i){var e=M(i).children("p");if(!(e.height()<=72)){var n=e.text(),s=Math.floor(e.width()/16);e.text(n.substr(0,3*s-1)+"...")}})}}.init(),{btn:null,target:null,isOpen:!1,input:null,init:function(){var t=this;this.btn=M(".news-filter-search-m i"),this.btn.length&&(this.target=M(".news-filter-search-m"),this.input=M(".news-filter-search-m input"),this.input.val(""),this.open=this.open.bind(this),this.close=this.close.bind(this),this.input.on("keypress",function(t){if(13!==t.which)return!0;var i=window.escape(t.target.value);return i=i.replace(/\+/g,"%2B"),window.location.href="/news/search?keyword="+i,!1}),this.btn.on("touchstart",function(i){if(t.isOpen){if(0===t.input.val().length)return;var e=window.escape(t.input.get(0).value);e=e.replace(/\+/g,"%2B"),window.location.href="/news/search?keyword="+e}else t.open();i.preventDefault(),i.stopPropagation()}),s&&(this.input.on("focus",function(){M(".header").hide()}),this.input.on("blur",function(){setTimeout(function(){M(".header").show()},300)})))},open:function(){var t=this;this.isOpen=!0,this.target.on("touch",function(t){t.stopPropagation(),t.preventDefault()}),this.target.addClass("open"),setTimeout(function(){M(window.document.body).on("touchstart",t.close)},300)},close:function(t){this.target.has(t.target).length||!this.target[0]===t.target||(this.isOpen=!1,this.input[0].blur(),this.input.val(""),this.target.removeClass("open"))}}.init(),{container:null,btn:null,target:null,isOpen:!1,init:function(){var t=this;this.btn=M(".news-tags-m-selected"),this.btn.length&&(this.target=M(".news-tags-m"),this.container=this.target.children("div"),this.open=this.open.bind(this),this.close=this.close.bind(this),this.scroll=this.scroll.bind(this),this.btn.on("click",function(){t.isOpen?t.close():t.open()}),this.container.on("click",o),this.target.on("click",this.close),this.target[0].addEventListener("touchstart",function(t){this.allowUp=this.scrollTop>0,this.allowDown=Math.ceil(this.scrollTop)<this.scrollHeight-this.clientHeight,this.lastY=t.touches[0].pageY}),this.target[0].addEventListener("touchmove",function(t){var i=t.touches[0].pageY>this.lastY,e=!i;i&&this.allowUp||e&&this.allowDown?t.stopPropagation():t.preventDefault(),this.allowUp=this.scrollTop>0,this.allowDown=Math.ceil(this.scrollTop)<this.scrollHeight-this.clientHeight,this.lastY=t.touches[0].pageY}))},open:function(){this.intervel=requestAnimationFrame(this.scroll),this.target.addClass("open"),M(".news-filter-m").on("touchmove",r),document.body.addEventListener("touchmove",r,{passive:!1}),this.isOpen=!0},close:function(){this.isOpen&&(this.target.removeClass("open"),document.body.removeEventListener("touchmove",r,{passive:!1}),M(".news-filter-m").off("touchmove",r),this.isOpen=!1,cancelAnimationFrame(this.intervel))},scroll:function(){window.scrollTo(0,240),this.intervel=requestAnimationFrame(this.scroll)}}.init();var S=function(){function t(t,i){for(var e=0;e<i.length;e++){var n=i[e];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}return function(i,e,n){return e&&t(i.prototype,e),n&&t(i,n),i}}();var E=window,D=E.$,I=E.tns;D(".about-activity").find(".image-gallery").each(function(t,i){new f(i).init()}),{items:[],init:function(){this.items=D(".about-members"),this.items.length&&this.items.each(function(t,i){var e=D(i).find(".about-member-extra");e.css({width:D(i).width()});var s=-1,a=D(i).find(".about-member");e.find("div:first-child").css("width",a.first().width());for(var o=0;o<a.length;o++)if(a.eq(o).hasClass("highlight")){s=o;break}for(var r=[],h=[],l=Math.ceil(a.length/4),c=0;c<l;c++){for(var u=0,d=0;d<4&&4*c+d<a.length;d++){var f=a.eq(4*c+d).find("h3").offset(),g=a.eq(4*c+d).find(".about-member-pos").offset(),p=f.height+g.height;h.push(p),p>u&&(u=p)}r.push(u)}for(var v=0;v<a.length;v++)h[v]=r[Math.floor(v/4)]-h[v];var m=n()?8:32;a.each(function(t,e){var n=D(e).find(".about-member-extra"),s=n.children("p"),a=n.children("div:first-child"),o=D(i).offset().left-s.offset().left;a.css({left:-o-m}),n.css({left:o})}),a.click(function(){var t=D(this),i=t.find(".about-member-extra"),e=a.index(this);a.eq(s).removeClass("highlight"),a.eq(s).find(".about-member-extra").css({height:0}),e!==s?(setTimeout(function(){if(s===e){t.addClass("highlight");var a=i.children("p");i.css({height:a.height()+(n()?8:28)+h[e],paddingTop:h[e]})}},-1===s?0:500),s=e):s=-1})})}}.init(),{container:[],init:function(){if(this.container=D(".about-comments-avatars"),this.container.length){var t=0,i=D(".about-comment"),e=D(".about-comments-avatar"),n=this.container.children("div");n.click(function(s){var a=n.index(this);a!==t&&(i.eq(t).addClass("hidden"),n.eq(t).removeClass("highlight"),t=a,i.eq(t).removeClass("hidden"),n.eq(t).addClass("highlight"),e.attr("src",D(s.target).attr("src")))})}}}.init(),{target:null,page:1,itemNum:0,container:null,waiting:!1,init:function(){var t=this;this.target=D("#load-more-activity"),this.target.length&&(this.itemNum=D(".about-activity").length,this.container=D(".about-activities"),this.target.click(function(){if(!t.waiting){var i=++t.page;t.waiting=!0,D.get("/about/atmosphere/activity?page="+i+"&pageSize=4",function(e){t.waiting=!1;var s=[];(t.itemNum+=e.data.length,t.itemNum===e.total&&t.target.addClass("hidden"),e.data.forEach(function(t){var e="",a=t.date.substr(0,4),o=t.date.substr(5,2),r="";if(t.imagePaths.length>0){var h="";if(t.imagePaths){h+='<div class="image-gallery-selector'+(1===t.imagePaths.length?" hidden":"")+'" data-type="carousel">';for(var l=0;l<t.imagePaths.length;l++)h+='<div class="'+(0===l?"highlight":"")+'"><img src="'+t.imagePaths[l]+'" /></div>';h+="</div>"}r+='<div class="gallery-section"><div class="image-gallery"><div class="image-gallery-current"><img src="'+t.imagePaths[0]+'" /></div>'+h+"</div></div>"}e+='<div class="about-activity" data-page=\''+i+"'><span>"+a+"年"+o+"月</span><h3>"+t.title+"</h3><p>"+t.content+"</h3>"+r+"</div>";var c=D(e);s.push(c),n()||new f(c).init()}),t.container.append(s),n())&&D(".about-activity[data-page='"+i+"']").find(".image-gallery-selector[data-type=carousel]").each(function(t,i){new g(i).init()})})}}))}}.init();var A=function(){function t(i){var e=this;!function(t,i){if(!(t instanceof i))throw new TypeError("Cannot call a class as a function")}(this,t),this.handleClick=function(){var t=e.isOpen?0:e.detailContent.height();e.isOpen=!e.isOpen,e.el.toggleClass("open"),e.detailContainer.css("height",t+"px")},this.destroy=function(){e.target.off("click",e.handleClick)},this.el=D(i),this.el.length&&(this.target=this.el.children(".about-hiring-item-header"),this.detailContainer=this.el.find(".about-hiring-item-detail"),this.detailContent=this.detailContainer.children("div"),this.isOpen=!1)}return S(t,[{key:"init",value:function(){this.target.on("click",this.handleClick)}}]),t}();D(".about-hiring-item").each(function(t,i){new A(i).init()}),{items:[],target:null,init:function(){var t=this;if(this.items=D(".about-contact-btns span"),this.items.length){var i=D(".about-banner"),e="",n=0;this.items.each(function(s,a){var o=D(a);o.on("click",function(){var s=o.data("place"),a=t.items.index(o);a!==n&&("hz"===s?e="关于我们-联系@2x.png":"sh"===s&&(e="关于我们-联系-上海.png"),i.css("background-image","url(/assets/images/banner/"+e),t.items.eq(n).removeClass("highlight"),o.addClass("highlight"),n=a)})})}}}.init(),{container:null,init:function(){this.container=D(".about-comments-m");var t=this.container.find(".about-comment-m");1===t.length&&this.container.css("padding","0 32px"),this.container.length&&1!==t.length&&I({container:this.container.get(0),items:1,slideBy:"page",controls:!1,nav:!1,swipeAngle:30,speed:300,gutter:t.length>1?16:0,edgePadding:t.length>1?16:0,loop:!1})}}.init();var H=function(){if(D(".about-historys").length){var t={};D(".about-histroy-year").each(function(i,e){var n=D(e);t[n.text()]?n.css("visibility","hidden"):t[n.text()]=!0})}};if(n()&&H(),D(".about-activity").find(".image-gallery").each(function(t,i){new f(i).init()}),n()&&D(".about-nav a").addClass("can-touch"),n()&&"#training"===location.hash){var Y=D("#training").offset().top-60;setTimeout(function(){window.scrollTo(0,Y)},100)}var j=function(){function t(t,i){for(var e=0;e<i.length;e++){var n=i[e];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}return function(i,e,n){return e&&t(i.prototype,e),n&&t(i,n),i}}();var B=window.$;({target:null,el:null,container:null,isShow:!1,init:function(){var t=this;this.container=B(".train-books"),this.el=B(".train-book-pur-list"),this.target=B("#purchase"),this.target.on("click",function(i){t.isShow?t.hidden():t.show(),i.preventDefault(),i.stopPropagation()}),this.hidden=this.hidden.bind(this)},show:function(){this.isShow=!0;var t=this.container.offset(),i=this.target.offset();this.target.children("svg").attr("transform","rotate(180 0 0)"),this.el.css({left:i.left-t.left,top:i.top-t.top+i.height}),this.el.removeClass("hidden"),B(document.body).on("click",this.hidden),B(document.body).on("touch",this.hidden)},hidden:function(){this.el.addClass("hidden"),this.target.children("svg").attr("transform","rotate(0 0 0)"),this.isShow=!1,B(document.body).off("click",this.hidden),B(document.body).off("touch",this.hidden)}}).init();var $=function(){function t(i){var e=this;!function(t,i){if(!(t instanceof i))throw new TypeError("Cannot call a class as a function")}(this,t),this.container=B(i),this.isOpen=this.container.hasClass("open"),this.target=B(i).find(".train-class-meta"),this.displayHeight=100,this.isOpen&&this.open(),this.target.on("click",function(){e.isOpen?e.close():e.open()})}return j(t,[{key:"open",value:function(){this.container.addClass("open"),this.container.css("max-height","500px"),this.isOpen=!0}},{key:"close",value:function(){this.container.removeClass("open"),this.container.css("max-height",this.displayHeight+"px"),this.isOpen=!1}}]),t}();B(".train-class").each(function(t,i){return new $(i)}),B(".train-sec-cases").find(".image-gallery").each(function(t,i){new f(i).init()});var L=window,U=L.$,_=L.tns;({containers:null,init:function(){this.containers=U(".tabs"),this.containers.length&&this.containers.each(function(t,i){var e=U(i).find(".image-gallery"),s=[];e.length>0&&e.each(function(t,i){var e=new f(i);e.init(),s.push(e)});var a=U(i).find(".tabs-container")[0],o=_({container:a,autoHeight:!0,items:1,slideBy:"page",controls:!1,nav:!1,speed:500,loop:!1,onInit:function(){s.forEach(function(t){t.cb=function(){var t=o.getInfo(),e=t.slideItems[t.index],n=U(e).height();U(i).find("#tns1-iw").css("height",n+"px")}})}});U(i).find(".tabs-item").css({opacity:1});var r=U(i).find(".tabs-selector"),h=U(r).children("div"),l=h.children("span");if(1===l.length)l.css("cursor","default");else{if(n()){var c=l.get().map(function(t,i){return i===l.length-1?0:U(t).width()+24}).reduce(function(t,i){return t+i},h.width()+32);h.css("width",c+"px")}l.each(function(t){l.eq(t).on("click",function(){o.goTo(t)})})}o.events.on("indexChanged",function(t){if(t.index!==t.indexCached){var i=l.eq(t.index);if(i.addClass("highlight"),l.eq(t.indexCached).removeClass("highlight"),n()){var e=h.offset().left;U(r).scrollLeft(i.offset().left-e)}}})})}}).init();var F=window.$;F.fn.isOnScreen=function(){var t=F(window),i={top:t.scrollTop()};i.bottom=i.top+t.height();var e=this.offset();return e.bottom=e.top+this.first().offsetHeight,!(i.bottom<e.top||i.top>e.bottom)},O(),n()&&F(".image-gallery-current[data-type=carousel]").each(function(t,i){new g(i).init()}),new function t(i){var e=this;!function(t,i){if(!(t instanceof i))throw new TypeError("Cannot call a class as a function")}(this,t),this.handler=function(){e.isRunning||(e.isRunning=!0,window.requestAnimationFrame?window.requestAnimationFrame(e.run):setTimeout(e.run,66))},this.run=function(){e.callbacks.forEach(function(t){return t()}),e.isRunning=!1},this.add=function(t){t&&e.callbacks.push(t)},this.callbacks=[],this.isRunning=!1,a(window).on(i,this.handler)}("scroll").add(q)}});