#lang racket

(require racket/port)
(require test-engine/racket-tests)

;; String -> [List String]
;; Extract all valid `mul`s from a string.
(define (extract-muls str)
  (regexp-match* #px"mul\\(\\d{1,3},\\d{1,3}\\)" str))


;; String -> Int
;; Extract the two numbers out of a `mul` and compute. 
(define (compute-mul mul)
  (apply * (map string->number (regexp-match* #px"\\d+" mul))))


;; String -> String
;; Remove all characters between `don't()` and `do()`.
(define (remove-dont str)
  (regexp-replace* #rx"don't\\(\\).*?do\\(\\)" str ""))


;; String Boolean-> Int
;; Compute the sum all `mul`s.
;; Ignore `don't()` blocks if `dont` is truthy.
(define (compute str dont)
  (apply + (map compute-mul (extract-muls (if dont (remove-dont str) str)))))


;; ([List Int] -> Int) Boolean Port -> Int
(define (solve-problem proc dont port)
  (proc (port->string port) dont))

;; Tests

(define given-test1
  "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))")

(define given-test2
  "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")

;; Part 1
(check-expect (solve-problem compute #f
                             (open-input-string given-test1))
                             161)

(check-expect (solve-problem compute #t
                             (open-input-string given-test2))
                             48)

(test)
