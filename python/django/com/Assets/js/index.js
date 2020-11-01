$(function () {
    $(".input input").focus(function () {
        $(this).parent(".input").each(function () {
            $("label", this).css({
                "line-height": "18px",
                "font-size": "18px",
                "font-weight": "100",
                "top": "0px"
            })
            $(".spin", this).css({
                "width": "100%"
            })
        });
    }).blur(function () {
        $(".spin").css({
            "width": "0px"
        })
        if ($(this).val() == "") {
            $(this).parent(".input").each(function () {
                $("label", this).css({
                    "line-height": "60px",
                    "font-size": "24px",
                    "font-weight": "300",
                    "top": "10px"
                })
            });

        }
    });


    $(".alt-2").click(function () {
        if (!$(this).hasClass('material-button')) {
            $(".shape").css({
                "width": "100%",
                "height": "100%",
                "transform": "rotate(0deg)"
            })

            setTimeout(function () {
                $(".overbox").css({
                    "overflow": "initial"
                })
            }, 600)

            $(this).animate({
                "width": "140px",
                "height": "140px"
            }, 500, function () {
                $(".box").removeClass("back");

                $(this).removeClass('active')
            });

            $(".overbox .title").fadeOut(300);
            $(".overbox .input").fadeOut(300);
            $(".overbox .button").fadeOut(300);

            $(".alt-2").addClass('material-buton');
        }

    });

    $(".material-button").click(function () {

        if ($(this).hasClass('material-button')) {
            setTimeout(function () {
                $(".overbox").css({
                    "overflow": "hidden"
                })
                $(".box").addClass("back");
            }, 200)
            $(this).addClass('active').animate({
                "width": "700px",
                "height": "700px"
            });

            setTimeout(function () {
                $(".shape").css({
                    "width": "50%",
                    "height": "50%",
                    "transform": "rotate(45deg)"
                });

                $(".overbox .title").fadeIn(300);
                $(".overbox .input").fadeIn(300);
                $(".overbox .button").fadeIn(300);
            }, 700)

            $(this).removeClass('material-button');

        }

        if ($(".alt-2").hasClass('material-buton')) {
            $(".alt-2").removeClass('material-buton');
            $(".alt-2").addClass('material-button');
        }
    });
    var log = document.getElementById('log');
    $('.head .lang .lang_m').click(function () {
        if (log.style.display == 'none') {
            log.style.display = '';
        } else {
            log.style.display = 'none'
        }
    });


    //注册框
    var phone = /^1\d{10}$/;
    var email = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;

    //注册账号输入
    $('#regname').focusout(function () {
        var name = $('#regname').val();
        if (phone.test(name) == false) {
            if (email.test(name) == false) {
                $('#r_u').html('请输入手机号或者邮箱！')
            } else {
                $('#r_u').html('');
            }
        } else {
            $('#r_u').html('');

        }
    });
    //注册密码输入
    $('#regpass').focusout(function () {
        if ($('#regpass').val().length < 8) {
            $('#r_p').html('密码长度应大于8!');
        } else {
            $('#r_p').html('');
        }
    });
    //确认密码输入
    $('#reregpass').focusout(function () {
        if ($('#reregpass').val() == $('#regpass').val()) {
            $('#r_pp').html('');
        } else {
            $('#r_pp').html('两次输入密码不一致');
        }
    });


    // 判断用户输入信息输入框输入完毕检测
    $(' #name').focusout(function () {
        var name = $('#name').val();
        if (phone.test(name) == false) {
            if (email.test(name) == false) {
                $('#l_u').html('请输入手机号或者邮箱！')
            } else {
                $('#l_u').html('');
                $('#l_mes').html('');
            }
        } else {
            $('#l_u').html('');

        }
    });
    //密码
    $('#pass').focusout(function () {
        if ($('#pass').val().length < 8) {
            $('#l_p').html('密码长度应大于8!');
        } else {
            $('#l_p').html('');
        }
    });

    //注册按钮点击
    $('#register').click(function () {
        if ($('#regname').val().length > 0 && $('#regpass').val().length > 7) {
            if (phone.test($('#regname').val()) == true || email.test($('#regname').val()) == true) {

                $('#r_mes').html('');
                var value = {
                    'account': $('#regname').val(),
                    'password': $('#regpass').val(),
                    "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
                };
                $.ajax({
                    type: 'POST',
                    url: '/regist/',
                    data: value,
                    timeout: 3000,
                    success: function (data) {
                        if (data.code == 200) {
                            $('#r_mes').html('注册成功!');
                        } else if (data.code == 300) {
                            $('#r_mes').html('账号已经存在!');
                        }

                        $('#regname').val('');
                        $('#regpass').val('');
                        $('#reregpass').val('');
                    },
                    error: function () {
                        $('#r_mes').html('注册失败!');
                    }
                })
            }
        } else {
            $('#r_mes').html('请检查输入内容！');
        }
    });
    //登录功能
    $('#login').click(function () {
        if ($('#name').val().length > 0 && $('#pass').val().length > 0) {
            $('#l_mes').html('');
            var value = {
                'account': $('#name').val(),
                'password': $('#pass').val(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            };
            $.ajax({
                type: 'POST',
                url: '/login/',
                data: value,
                timeout: 3000,
                success: function (data) {
                    if (data.code == 200) {
                        var preUrl = window.location.href;
                        if (data.data) {
                            window.open(preUrl, '_parent');
                        }
                    } else if (data.code == 300) {
                        $('#l_mes').html('密码输入错误!');
                        $('#pass').val('');

                    } else if (data.code == 400) {
                        $('#l_mes').html('账号不存在!');
                        $('#pass').val('');
                        $('#name').val('');
                    }
                },
                error: function () {
                    $('#l_mes').html('登录失败！');
                }
            });

        } else {
            $('#l_mes').html('请检查输入内容!')
        }
    })

});

