// 1 ya khud se divisible

const n = 9;

function isPrime(num) {
    for (let i = 2; i < num; i++) {
        if (num % i == 0) {
            console.log("Not prime");
            return;
        }
    }

    console.log("Prime");
}

isPrime(n);