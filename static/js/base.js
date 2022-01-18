

// to check image field is empty or not
function checkBtn() {
    let post = document.getElementById('post');
    let addPostBtn = document.getElementById('addPostBtn');
    let file = post.files[0]
    if (file) {
        addPostBtn.disabled = false;
        let previewContainer = document.getElementById('preview-container');
        previewContainer.style.display = "block";
        const reader = new FileReader();
        let imagePreview = document.getElementById('image-preview')
        reader.addEventListener("load", function () {
            imagePreview.setAttribute('src', this.result)
        });
        reader.readAsDataURL(file)
    } else {
        addPostBtn.disabled = true;

    }
}

// csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// show profile
function showProfile(username) {
    var base_url = window.location.origin;
    url = `${base_url}/profile/${username}`
    window.location.href = url;
}

// search
function search() {
    let username = document.getElementById('searchUser').value
    var base_url = window.location.origin;
    let url = base_url + '/test'

    let result;
    fetch(url, {
        method: "POST",
        body: JSON.stringify({
            'username': username
        }),
        headers: {
            'X-CSRFToken': csrftoken,
            "Content-type": "application/json; charset=UTF-8"
        }
    })
        .then(res => {
            return res.json()
        })
        .then(out => {
            // console.log('Checkout this JSON! ', out),
            if (out.length == 0) {
                document.getElementById('searchUser').setAttribute('data-content', 'no user found')
            } else {
                result = `<table class="table table-hover table-white">
                <tbody>`
                out.forEach(user => {
                    result += `<tr onClick="showProfile('${user.username}')" class="hover-effect">               
                                <td>${user.username}</td>
                                <td><img class="img-search mx-2 " src='${base_url}/media/${user.profileImage}' alt="" style="border-radius: 100%;"></td>
                                </tr>`
                });
                result += `</tbody>
              </table>`
                document.getElementById('searchUser').setAttribute('data-content', result)
            }
        })
        .catch(err =>err)
        .finally()

    // show popover for search results
    $('#searchUser').popover('show');
}
$.fetch({
    cache: false,
  });

