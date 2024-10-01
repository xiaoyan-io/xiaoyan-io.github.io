var posts=["2024/10/01/clash规则配置文件-1/","2024/10/01/openwrt/","2024/10/01/clash规则配置文件/","2024/09/15/hello-world/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };