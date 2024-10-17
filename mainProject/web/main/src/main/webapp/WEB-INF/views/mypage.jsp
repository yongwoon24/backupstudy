<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@ page session="true" %>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>테스트 쇼핑몰 페이지 - 마이페이지</title>
    <link rel="stylesheet" href="https://s3.ap-northeast-2.amazonaws.com/materials.spartacodingclub.kr/easygpt/default.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4"
        crossorigin="anonymous"></script>
    <script>
        // 로그인 알림 및 리다이렉트 처리
        window.onload = function() {
            if (${loginRequired}) {
                alert("로그인이 필요합니다.");
                window.location.href = "/login"; // 로그인 페이지로 리다이렉트
            }
        }
    </script>
    <style>
    .icon-link {
            position: absolute;
            top: 20px;
            right: 20px;
            text-decoration: none;
            color: white;
        }
        .icon-link i {
            font-size: 2rem;
        }
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
        <h2 class="text-center mb-4">마이페이지</h2>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">내 정보</h5>
                <!-- 세션에서 가져온 유저 정보를 출력 -->
                <c:choose>
                    <c:when test="${not empty sessionScope.user}">
                        <p class="card-text">이름: ${sessionScope.user.username}</p>
                        <p class="card-text">이메일: ${sessionScope.user.email}</p>
                        <p class="card-text">유저등급: ${sessionScope.user.grade}</p>
                    </c:when>
                    <c:otherwise>
                        <p>로그인 정보가 없습니다. 로그인 해주세요.</p>
                    </c:otherwise>
                </c:choose>
                <a href="/edit-profile" class="btn btn-primary">프로필 수정</a>
                <a href="/logout" class="btn btn-secondary">로그아웃</a>
            </div>
            
        </div>
         <!-- 주문 내역 표시 -->
    <div class="mt-4">
        <h5>주문 내역</h5>
        <c:choose>
            <c:when test="${not empty orders}">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>주문 번호</th>
                            <th>주문 날짜</th>
                            <th>총 금액</th>
                        </tr>
                    </thead>
                    <tbody>
                        <c:forEach var="order" items="${orders}">
                            <tr>
                                <td><a href="/order/${order.orderId}/items">${order.orderId}</a></td>
                                <td><fmt:formatDate value="${order.orderDate}" pattern="yyyy-MM-dd"/></td>
                                <td>₩${order.totalPrice}</td>
                            </tr>
                        </c:forEach>
                    </tbody>
                </table>
            </c:when>
            <c:otherwise>
                <p>주문 내역이 없습니다.</p>
            </c:otherwise>
        </c:choose>
    </div>
    </div>

</body>

</html>
