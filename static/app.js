//For search bar in layout.html
function changeSearchType(option){

    searchBar = document.querySelector("#search_bar");

    if(option == "posts"){

        searchBar.placeholder = "Search Posts";

    }else if(option == "users") {

        searchBar.placeholder = "Search Users";

    }
}

//For user's view in profile.html
document.querySelector(".profile_nav").addEventListener("click", function(e){

    var target = e.target;

    var profileView = document.querySelector(".profile_view");
    var likedPosts = document.querySelector(".profile_liked");
    var dislikedPosts = document.querySelector(".profile_disliked");
    var userPosts = document.querySelector(".profile_posts");


        if(target.getAttribute('id') == "profile"){

            profileView.style.display = "flex";
            likedPosts.style.display = "none";
            dislikedPosts.style.display = "none";
            userPosts.style.display = "none";

        } else if (target.getAttribute('id') == "liked_posts"){

            likedPosts.style.display = "flex";
            profileView.style.display = "none";
            dislikedPosts.style.display = "none";
            userPosts.style.display = "none";

        } else if (target.getAttribute('id') == "disliked_posts"){

            dislikedPosts.style.display = "flex";
            profileView.style.display = "none";
            likedPosts.style.display = "none";
            userPosts.style.display = "none";

        } else if (target.getAttribute('id') == "posts"){

            userPosts.style.display = "flex";
            profileView.style.display = "none";
            likedPosts.style.display = "none";
            dislikedPosts.style.display = "none";

        }

});