<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ page session="false" %>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>테스트 쇼핑몰 페이지</title>
    <link rel="stylesheet" href="https://s3.ap-northeast-2.amazonaws.com/materials.spartacodingclub.kr/easygpt/default.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4"
        crossorigin="anonymous"></script>
    <style>
        .carousel-item {
            padding: 20px;
        }
        .carousel-inner {
            display: flex;
            align-items: center;
        }
        .carousel-item img {
            max-width: 100%;
            height: auto;
        }
        .icon-link {
            position: absolute;
            top: 20px;
            right: 20px;
            text-decoration: none;
            color: white;
        }
        .icon-link i {
            font-size: 2rem;
    </style>
</head>

<body>
	<!-- 헤더 시작 -->
	<div class="hero d-flex align-items-center justify-content-center" style="background-color: #333333; position: relative;">
    <div class="container text-center">
        <h1 class="display-4 text-light">Computer Peripherals Online Store</h1>
        <!-- <p class="lead text-light">test</p> -->
    </div>
    <!-- 마이페이지 링크 추가 -->
    <a href="/mypage" class="position-absolute" style="top: 20px; right: 20px; text-decoration: none;">
        <i class="bi bi-person-circle text-light" style="font-size: 2rem;"></i>
        <!-- <span class="text-light"></span> -->
    </a>
     <!-- 장바구니 링크 추가 -->
        <a href="/cart" class="icon-link" style="right: 80px;">
            <i class="bi bi-cart"></i>
        </a>
</div>


    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">컴퓨터쇼핑몰</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Products
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <li><a class="dropdown-item" href="#">Mouse</a></li>
                            <li><a class="dropdown-item" href="#">Keyboard</a></li>
                            <li><a class="dropdown-item" href="#">Monitor</a></li>
                            <li><a class="dropdown-item" href="#">Webcam</a></li>
                            <li><a class="dropdown-item" href="#">Speaker</a></li>
                            <li><a class="dropdown-item" href="#">HeadPhone</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/products">All products</a></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">About Us</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Contact</a></li>
                </ul>
                <form class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>
    <!-- 헤더 끝 -->

   <div class="container mt-5">
        <h2 class="text-center mb-4">로그인</h2>
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card p-4">
                    <form action="/login" method="post">
                        <div class="mb-3">
                            <label for="email" class="form-label">이메일</label>
                            <input type="email" class="form-control" id="email" name="email" placeholder="이메일을 입력하세요" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">비밀번호</label>
                            <input type="password" class="form-control" id="password" name="password" placeholder="비밀번호를 입력하세요" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">로그인</button>
                    </form>
                    <div class="text-center mt-3">
                        <a href="/signup">회원가입</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

</body>

</html>
