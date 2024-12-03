#lang racket

;; Port (String X -> X) X
;; Folds a function over the lines from a file.
(define (read-lines port op initial)
  (let ([lines (port->lines port)])
    (foldr op initial lines)))

;; Port (String -> X) String Int -> [List [List X]]
(define (read-columns port itemwise-op sep n-cols)
  (read-lines port
              (λ(line acc)
                (map (λ(item acc-list) (cons (itemwise-op item) acc-list))
                     (string-split line sep)
                     acc))
              (build-list n-cols (λ(_) '()))))


;; Port (String -> X) String -> [List [List X]]
(define (read-rows port itemwise-op sep)
  (read-lines port
              (λ(line acc)
                (cons (map itemwise-op
                           (string-split line sep))
                      acc))
              '()))

(provide read-columns
         read-rows
         read-lines)