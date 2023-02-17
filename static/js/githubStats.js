$.get('https://api.github.com/repos/mage2gen/Mage2Gen', function (res) {
    if (res) {
        $('#github-stars span.counter').text(res.stargazers_count)
        $('#github-forks span.counter').text(res.forks_count)
    }
});