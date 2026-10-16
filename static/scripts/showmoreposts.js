const posts_container = document.getElementById("posts-container")
const showmorepost = document.getElementById("showmorepost")

const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        loadPosts()
    }
}, {
    rootMargin: "300px"
});

function observePosts() {
    observer.disconnect();

    const posts = document.querySelectorAll(".post");

    if (posts.length >= 3) {
        observer.observe(posts[posts.length - 1]);
    }
}

observePosts();


async function loadPosts() {
    const posts = document.querySelectorAll(".post");
    const url = posts_container.dataset.url
    const last_id = posts[posts.length - 1].getAttribute("data-id")
    showmorepost.className = "showmore"


    const response = await fetch(url, {
        method:"POST",
        headers:{
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            last_id:last_id
        })
    });


    const data = await response.json()

    if (data.success){
        showmorepost.className = "showmore showmore-deactive"

        for (const post of data.posts) {

            let post_element = `
                <div class="post" data-id="${post.id}">
                    <div class="post-header">
                        <div class="left">
                            <div class="avatar">
                                <img 
                                    src="${post.avatar ? post.avatar : '/static/images/default-avatar.png'}" 
                                    alt="${post.username}" 
                                    draggable="false"
                                >
                            </div>
                            <div class="account-info"> 
                                <h2>
                                    <a href="/@${post.username}">@${post.username}</a>
                                </h2>
                                
                                    <h3>${post.fullname}</h3>
                                
                            </div>
                        </div>
                        <div class="right">
                            <div class="dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            <div class="post-dropdown"></div>
                        </div>
                    </div>
                    <div class="post-body">
                        <div class="foreign-lang">
                            <div class="flag">
                                <img src="/static/images/${post.lang.toLowerCase()}.png" draggable="false" alt="${post.lang}">
                            </div>
                            <div class="content">
                                <div class="lang">${post.lang}</div>
                                <div class="sentence">${post.sentence}</div>
                            </div>
                        </div>
        
                        <div class="description">
                            <div div="" class="flag">
                                <img src="/static/images/az.png" draggable="false" alt="AZ">
                            </div>
                            <div class="content">
                                <div class="lang">AZ</div>
                                <div class="sentence">${post.description}</div>
                            </div>
                        </div>
                    </div>
                    <div class="like-created">
                        <div class="like" ${post.is_authenticated ? '' : 'onclick="window.location.href=\'/login\'"'}>
                            <i class="${post.is_liked ? 'fa-solid fa-heart' : 'fa-regular fa-heart'}"
                                ${post.is_authenticated && ! post.is_liked ? 'onclick="postLike(this)"' : ''}
                                data-id="${post.id}"
                                data-url="/post/post-like/">
                            </i>
                            <span>${post.likes}</span>
                        </div>
                        <div class="dot"></div>
                        <div class="view">
                            <i class="fa-solid fa-eye"></i>
                            <span>${post.view}</span>
                        </div>
                        <div class="dot"></div>
                        <div class="created">
                            ${post.smartdate} paylaşılıb
                        </div>
                    </div>
                    <div class="btn-group">
                        <a href="/post/${post.slug}"><i class="fa-brands fa-leanpub"></i> Ətraflı bax</a>
                    </div>
                </div>
            `
            
            posts_container.innerHTML += post_element
        }

        if (data.has_more){
            observePosts()
        }

    }



    
}