var posts=["2024/10/23/群晖使用docker部署joplin/","2024/10/23/G-Box-安装使用说明/","2024/10/22/新的文章/","2024/10/20/hello-world/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };