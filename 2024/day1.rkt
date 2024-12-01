#lang racket

(require "utils/utils.rkt")
(require test-engine/racket-tests)

;; Part 1

;; [List [List Number]] -> Number
(define (total-distance lists)
  (apply +                                       ;; Sum of...
         (apply map (compose abs -)              ;; distances of...
                (map (λ(l) (sort l <)) lists)))) ;; sorted lists.

(define (solve-problem proc port)
  (proc (read-columns port string->number "   " 2)))


;; Part 2

;; [List X] -> [List [Pair X Integer]]
;; The absolute frequency distribution of a list
(define (frequencies lst)
  (map (λ(v) (cons v (count (λ(x) (= x v)) lst))) (remove-duplicates lst)))

;; [List [List Number]] -> Number
(define (total-similarity-score lists)
  (let ([freqs (frequencies (second lists))])
    (apply +                                  ;; Sum of...
           (map (λ(v)                        
                  (* v                        ;; items times...
                     (cdr (or (assoc v freqs) ;; their frequencies...
                              (cons v 0)))))
                (first lists)))))             ;; for each item in the list.

;; Tests
(define given-test
"3   4
4   3
2   5
1   3
3   9
3   3")

(check-expect (solve-problem total-distance
                             (open-input-string given-test))
              11)

(check-expect (solve-problem total-similarity-score
                             (open-input-string given-test))
              31)
(test)