<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ERP 시스템</title>
<link rel="stylesheet"
    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script
    src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
<script
    src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
    rel="stylesheet"
    integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
    crossorigin="anonymous">
</head>
<body>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">ERP 시스템</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <a class="nav-link" href="/erp/dashboard">대시보드</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/erp/productList">재고 관리</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/erp/userList">고객 관리</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/erp/orders">주문 내역 관리</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="salesAnalysisDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        판매 분석
                    </a>
                    <div class="dropdown-menu" aria-labelledby="salesAnalysisDropdown">
                        <a class="dropdown-item" href="/erp/sales-analysis-all">전체</a>
                        <a class="dropdown-item" href="/erp/sales-analysis-category">카테고리별</a>
                        <a class="dropdown-item" href="/erp/sales-analysis-brand">브랜드별</a>
                        <a class="dropdown-item" href="/erp/sales-analysis-product">품목별</a>
                    </div>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/erp/ocr">OCR 관리</a>
                </li>
                 <li class="nav-item">
                    <a class="nav-link" href="#">EVENT 관리</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/erp/report">보고서</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container mt-4">
    
        <!-- 사용자 입력 영역 -->
        <div class="text-center mb-4">
            <label for="startDate">시작 날짜:</label>
            <input type="date" id="startDate" class="form-control" style="display:inline-block; width:auto;">
            
            <label for="endDate">종료 날짜:</label>
            <input type="date" id="endDate" class="form-control" style="display:inline-block; width:auto;">
            
            <label for="periodType">분석 기준:</label>
            <select id="periodType" class="form-select" style="display:inline-block; width:auto;">
                <option value="DAILY">일간</option>
                <option value="WEEKLY">주간</option>
                <option value="MONTHLY">월간</option>
            </select>
            
            <button id="loadData" class="btn btn-primary">조회</button>
        </div>

        <!-- 판매량 차트 및 테이블 -->
        <div class="row">
            <div class="col-md-6">
                <h3 class="text-center">전체 판매량</h3>
                <canvas id="salesChart" name="salesChart" width="400" height="200"></canvas>
                <table class="table table-striped mt-4">
                    <thead>
                        <tr><th>날짜</th><th>총 판매량</th></tr>
                    </thead>
                    <tbody id="salesTableBody"></tbody>
                </table>
            </div>
            
            <!-- 매출액 차트 및 테이블 -->
            <div class="col-md-6">
                <h3 class="text-center">전체 매출액</h3>
                <canvas id="revenueChart" name="revenueChart" width="400" height="200"></canvas>
                <table class="table table-striped mt-4">
                    <thead>
                        <tr><th>날짜</th><th>총 매출액</th></tr>
                    </thead>
                    <tbody id="revenueTableBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
    let salesChart = null;
    let revenueChart = null;

    function getTodayDate() {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    $(document).ready(function () {
        const startDate = '2024-09-01';
        const today = getTodayDate();

        $('#startDate').val(startDate);
        $('#endDate').val(today);

        loadSalesAndRevenueData(startDate, today, 'DAILY');

        $('#loadData').click(function () {
            const selectedStartDate = $('#startDate').val();
            const selectedEndDate = $('#endDate').val();
            const periodType = $('#periodType').val();

            if (selectedStartDate && selectedEndDate) {
                $('#periodDate').text(selectedStartDate + ' ~ ' + selectedEndDate);
                loadSalesAndRevenueData(selectedStartDate, selectedEndDate, periodType);
            } else {
                alert('시작 날짜와 종료 날짜를 선택해 주세요.');
            }
        });
    });

    function loadSalesAndRevenueData(startDate, endDate, periodType) {
        $.ajax({
            url: '/erp/total-sales-revenue',
            type: 'GET',
            data: { startDate: startDate, endDate: endDate, periodType: periodType },
            success: function(response) {
                const salesData = response.map(item => item.TOTAL_QUANTITY || 0);
                const revenueData = response.map(item => item.TOTAL_REVENUE || 0);

                const labels = response.map(item => {
                    const timestamp = item.PERIOD;
                    if (!timestamp) {
                        return '-- ~ --';
                    }

                    const date = new Date(timestamp);

                    if (periodType === 'WEEKLY') {
                        const weekNumber = getWeekNumberOfYear(date);
                        return weekNumber + '주차';
                    } else {
                        const year = date.getFullYear();
                        const month = date.getMonth() + 1;
                        const day = date.getDate();

                        const formattedMonth = String(month).padStart(2, '0');
                        const formattedDay = String(day).padStart(2, '0');

                        return year + '-' + formattedMonth + '-' + formattedDay;
                    }
                });

                if (salesChart) {
                    salesChart.destroy();
                    salesChart = null;
                }
                if (revenueChart) {
                    revenueChart.destroy();
                    revenueChart = null;
                }

                const salesCtx = document.getElementById('salesChart').getContext('2d');
                salesChart = new Chart(salesCtx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: '총 판매량',
                            data: salesData,
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            fill: true,
                            borderWidth: 2,
                            tension: 0.3
                        }]
                    },
                    options: { scales: { y: { beginAtZero: true } } }
                });

                const revenueCtx = document.getElementById('revenueChart').getContext('2d');
                revenueChart = new Chart(revenueCtx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: '총 매출액',
                            data: revenueData,
                            backgroundColor: 'rgba(153, 102, 255, 0.2)',
                            borderColor: 'rgba(153, 102, 255, 1)',
                            fill: true,
                            borderWidth: 2,
                            tension: 0.3
                        }]
                    },
                    options: { scales: { y: { beginAtZero: true } } }
                });

                let salesTableBody = '';
                let revenueTableBody = '';
                for (let i = 0; i < labels.length; i++) {
                    salesTableBody += '<tr><td>' + labels[i] + '</td><td>' + salesData[i] + '</td></tr>';
                    revenueTableBody += '<tr><td>' + labels[i] + '</td><td>' + revenueData[i] + '</td></tr>';
                }
                $('#salesTableBody').html(salesTableBody);
                $('#revenueTableBody').html(revenueTableBody);
            },
            error: function(error) {
                console.error('데이터 로드 중 오류 발생:', error);
            }
        });
    }

    // 연도 기준으로 몇 번째 주차인지 계산하는 함수
    function getWeekNumberOfYear(date) {
        const startOfYear = new Date(date.getFullYear(), 0, 1);
        const days = Math.floor((date - startOfYear) / (24 * 60 * 60 * 1000));
        const weekNumber = Math.ceil((days + startOfYear.getDay() + 1) / 7);
        return weekNumber;
    }
    </script>
</body>
</html>

