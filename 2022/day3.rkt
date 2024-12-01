;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname day3) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
(require racket/string)
(require racket/list)
(require racket/base)

;; String --> Num
(define (sum-badges str)
  (find-badges (string-split str "\n") 0))

;; LoStr --> Num
(define (find-badges los sum)
  (cond [(empty? los) sum]
        [(cons? los) (find-badges (list-tail los 3) (+ sum
                      (get-priority (find-repeated-char (map string->list (take los 3))))))]))

;; String --> Num
(define (sum-priorities str) (foldr (λ(x acc) (+ acc (priority x))) 0 (string-split str "\n")))

;; LoLoChar --> Char
(define (find-repeated-char loloc) (foldr (λ(x acc) (if (andmap (λ(lst) (member? x lst)) (rest loloc)) x acc)) #\a (first loloc)))

;; String --> Num
(define (priority str)
  (get-priority (find-repeated-char (list (first-half (string->list str)) (second-half (string->list str))))))

;; LoChar --> LoChar
(define (first-half loc)
  (take loc (/ (length loc) 2)))

;; LoChar --> LoChar
(define (second-half loc)
  (list-tail loc (/ (length loc) 2)))

;; Char --> Num
(define (get-priority c)
  (add1 (index-of (string->list "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") c)))