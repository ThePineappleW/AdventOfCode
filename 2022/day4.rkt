;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname day4) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
(require racket/string)

(define-struct range* (lo hi))

;; String -> Num
(define (count str pred)
  (foldr (λ(x acc) (if (pred x) (add1 acc) acc)) 0 (split-to-pairs str)))

;; Pair-of Range --> Bool
(define (contains-complete pr)
  (or (<= (range*-lo (first pr)) (range*-lo (second pr)) (range*-hi (second pr)) (range*-hi (first pr)))
      (<= (range*-lo (second pr)) (range*-lo (first pr)) (range*-hi (first pr)) (range*-hi (second pr)))))

;; Pair-of Range --> Bool
(define (overlap pr)
  (range-overlap (first pr) (second pr)))

;; Range Range --> Bool
(define (range-overlap r1 r2)
  (or (<= (range*-lo r1) (range*-lo r2) (range*-hi r1))
      (<= (range*-lo r2) (range*-lo r1) (range*-hi r2))))

;; =================================
;; Input processing

;; String --> LoLoRange
(define (split-to-pairs input)
  (map to-pair (string-split input "\n")))

;; String x-y,z-a --> LoLoRange ((x,y) (z,a))
(define (to-pair str) (map string->range (sep-pair str)))

;; String --> LoStr
(define (sep-pair str) (string-split str ","))

;; String --> Range
;; lo-hi --> (make-range* lo hi)
(define (string->range str)
  (make-range* (string->number (first (string-split str "-")))
              (string->number (second (string-split str "-")))))