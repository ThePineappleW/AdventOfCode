;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname day6) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require racket/base)
(require racket/list)

;; String --> Number
(define (find-first-index str)
  (find-first-unique (string->list str) 0))

;; LoC --> LoC
(define (all-unique? loc)
  (andmap (λ(c) (= 1 (length (filter (λ(x) (char=? x c)) loc)))) loc))

;; String --> Num
(define (find-first-unique loc start len)
  (cond [(<= (length loc) (sub1 len)) -1]
        [(all-unique? (take loc len)) (+ len start)]
        [else (find-first-unique (rest loc) (add1 start))]))