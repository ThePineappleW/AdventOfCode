;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname day7) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require racket/base)
(require racket/list)
(require racket/string)

(define-struct dir (name parent files dirs))
(define-struct file (name size))
(define-struct parser-state (cur tree hist))

;; String --> Dir
(define (parse-input str)
  (parser-state-tree (foldl (λ(s state) (update-parser-state state s))
                            (make-parser-state "/" (make-dir "/" "" '() '()) '())
                            (rest* (string-split str "\n")))))


;; ParserState String --> ParserState
(define (update-parser-state ps str)
  (let ([data (string-split str " ")]) ;; LoString 
    (cond [(cmd? data) (handle-command ps (rest data))]
          [else (update-ps ps data)])))

;; ParserState LoStr --> ParserState 
(define (handle-command ps los)
  (let ([name (first los)]
        [arg (rest los)])
    (cond [(string=? name "ls") ps]
          [(string=? name "cd") (handle-cd ps (first arg))])))

;; ParserState str --> ParserState
(define (handle-cd ps arg)
  (cond [(string=? arg "..")
         (make-parser-state
          (first (parser-state-hist ps))
          (parser-state-tree ps)
          (rest* (parser-state-hist ps)))]
        [(string=? arg "\\")
         (make-parser-state
          "\\")
         (parser-state-tree ps)
         '()]
        [else (make-parser-state
               (string-append (parser-state-cur ps) arg)
               (parser-state-tree ps)
               (cons (parser-state-cur ps) (parser-state-hist ps)))]))

;; ParserState LoStr --> ParserState
(define (update-ps ps data)
  (cond [(numeric? (first data)) (make-parser-state
                                  (parser-state-cur ps)
                                  (insert-to-dir (parser-state-tree ps)
                                                 (parser-state-cur ps)
                                                 (los->file data))
                                  (parser-state-hist ps))]
        [(string=? "dir" (first data)) (make-parser-state
                                        (parser-state-cur ps)
                                        (insert-to-dir (parser-state-tree ps)
                                                       (parser-state-cur ps)
                                                       (los->dir data (parser-state-cur ps)))
                                        (parser-state-hist ps))]))

;; Dir String File/Dir --> Dir
(define (insert-to-dir dir parent-name obj)
  (if (string=? parent-name (dir-name dir))
      (cond [(file? obj) (make-dir
                          (dir-name dir)
                          (dir-parent dir)
                          (cons obj (dir-files dir))
                          (dir-dirs dir))]
            [(dir? obj) (make-dir
                         (dir-name dir)
                         (dir-parent dir)
                         (dir-files dir)
                         (cons obj (dir-dirs dir)))])
      (make-dir
       (dir-name dir)
       (dir-parent dir)
       (dir-files dir)
       (map (λ(x) (insert-to-dir x parent-name obj)) (dir-dirs dir)))))


;; LoString --> File
(define (los->file los)
  (make-file (second los) (string->number (first los))))

;; LoString String --> Dir
(define (los->dir los parent)
  (make-dir (string-append parent (second los)) parent '() '()))

;; String --> Bool
(define (cmd? los)
  (string=? "$" (first los)))

;; String --> Bool
(define (numeric? str)
  (regexp-match? #rx"^[0-9]+$" str))

;; Dir Num --> Num
(define (sum-file-sizes dir max-size) ;; inclusive
  (foldr (λ(d acc) (+ (sum-file-sizes d max-size) acc))
         (if (<= (dir-size dir) max-size) (dir-size dir) 0)
         (dir-dirs dir)))

;; Dir --> Num
(define (dir-size dir)
  (+ (foldr (λ(f acc) (+ (file-size f) acc)) 0 (dir-files dir))
     (foldr (λ(d acc) (+ (dir-size d) acc)) 0 (dir-dirs dir))))

;; Str --> Num
(define (count-dir-sizes str)
  (sum-file-sizes (parse-input str) 100000))

;; Str --> Num
(define (find-smallest-to-delete str)
  (let* ([tree (parse-input str)]
         [unused-space (- 70000000 (dir-size tree))]
         [to-free (- 30000000 unused-space)])
    (dir-size (get-smallest tree to-free))))

;; Dir Num --> Dir
(define (get-smallest dir threshold)
  (first
   (filter
    (λ(x) (>= (dir-size x) threshold))
    (sort
     (get-all-dirs dir)
     (λ(d1 d2) (< (dir-size d1) (dir-size d2)))))))

;; Dir --> LoDir
(define (get-all-dirs dir)
  (cond [(empty? (dir-dirs dir)) (list dir)]
        [(cons? (dir-dirs dir)) (flatten (append (list dir) (map get-all-dirs (dir-dirs dir))))]))

;; LoX --> LoX
(define (rest* lst)
  (if (empty? lst) '() (rest lst)))