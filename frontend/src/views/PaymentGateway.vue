<template>
    <div class="container">
        <div class="row">
            <div class="col-xs-12 col-md-4">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">Payment Details</h3>
                        <div class="checkbox pull-right">
                            <label><input type="checkbox" /> Remember</label>
                        </div>
                    </div>
                    <div class="panel-body">
                        <form role="form">
                            <div class="form-group">
                                <label for="cardNumber">CARD NUMBER</label>
                                <div class="input-group">
                                    <input type="text" class="form-control" id="cardNumber" v-model="cardNumber" placeholder="Valid Card Number" required autofocus />
                                    <span class="input-group-addon"><span class="glyphicon glyphicon-lock"></span></span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-xs-7 col-md-7">
                                    <div class="form-group">
                                        <label for="expityMonth">EXPIRY DATE</label>
                                        <div class="col-xs-6 col-lg-6 pl-ziro">
                                            <input type="text" class="form-control" id="expityMonth" v-model="expiryMonth" placeholder="MM" required />
                                        </div>
                                        <div class="col-xs-6 col-lg-6 pl-ziro">
                                            <input type="text" class="form-control" id="expityYear" v-model="expiryYear" placeholder="YY" required />
                                        </div>
                                    </div>
                                </div>
                                <div class="col-xs-5 col-md-5 pull-right">
                                    <div class="form-group">
                                        <label for="cvCode">CV CODE</label>
                                        <input type="password" class="form-control" id="cvCode" v-model="cvCode" placeholder="CV" required />
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <ul class="nav nav-pills nav-stacked">
                    <div class="form-group">
                        <label for="DownloadPrice">ENTER DOWNLOAD PRICE</label>
                        <div class="input-group">
                            <input type="text" class="form-control" id="DownloadPrice" v-model="downloadPrice" placeholder="Valid DownloadPrice" required autofocus />
                            <span class="input-group-addon"><span class="glyphicon glyphicon-lock"></span></span>
                        </div>
                    </div>
                </ul>
                <br />
                <button :disabled="isPaid" @click="processPayment" class="btn btn-success btn-lg btn-block" role="button">Pay</button>
                <a v-if="isPaid" @click="onDownloadClick" :href="downloadLink" class="btn btn-warning btn-lg btn-block" role="button">
                    Download
                </a>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
    name: 'PaymentGateway',
    data() {
        return {
            cardNumber: '',
            expiryMonth: '',
            expiryYear: '',
            cvCode: '',
            bookId: this.$route.query.book_id,
            downloadPrice: parseFloat(this.$route.query.downloadPrice),
            isPaid: false,
            downloadLink: ''
        };
    },
    methods: {
        async processPayment() {
            try {
                const response = await axios.post('http://localhost:5000/api/payment', {
                    book_id: this.bookId,
                    cardNumber: this.cardNumber,
                    expiryMonth: this.expiryMonth,
                    expiryYear: this.expiryYear,
                    cvCode: this.cvCode,
                    downloadPrice: this.downloadPrice
                });

                if (response.status === 200) {
                    this.isPaid = true;
                    this.downloadLink = `http://localhost:5000/api/ebooksDownload/${this.bookId}/pdf`;
                    Swal.fire({
                        icon: 'success',
                        title: 'Payment Completed',
                        text: 'Payment completed. Kindly download your book.',
                        confirmButtonText: 'OK'
                    });
                }
            } catch (error) {
                console.error('Payment failed:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Payment Failed',
                    text: 'Payment failed. Please try again.',
                    confirmButtonText: 'OK'
                });
            }
        },
        onDownloadClick(event) {
            event.preventDefault(); // Prevent the default anchor click behavior

            Swal.fire({
                title: 'Download in Progress',
                text: 'Please wait while we download the book.',
                allowOutsideClick: false,
                didOpen: () => {
                    // Create an invisible iframe to start the download
                    const iframe = document.createElement('iframe');
                    iframe.style.display = 'none';
                    iframe.src = this.downloadLink;
                    document.body.appendChild(iframe);

                    // Show alert after download
                    Swal.fire({
                        icon: 'success',
                        title: 'Download Completed',
                        text: 'Your book has been downloaded successfully.',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        this.redirectToUserIssuedBooksView();
                    });
                }
            });
        },
        redirectToUserIssuedBooksView() {
            this.$router.push({ name: 'userissuedbooksview' });
        }
    }
};
</script>

    
<style>
body {
    margin-top: 20px;
}

.panel-title {
    display: inline;
    font-weight: bold;
}

.checkbox.pull-right {
    margin: 0;
}

.pl-ziro {
    padding-left: 0px;
}
</style>
