### Student Name: Arlen Smith
### Student Number: 20386063
### Group Number: 4

# Part B:

|-----------------------------------|---------------------------|---------------------------------------------|
|         **Function Name**         | **Implementation Status** |             **What is Missing**             |
|-----------------------------------|---------------------------|---------------------------------------------|
|                                   |                           | An ISBN number of any set of exactly 13     |
|        add_book_to_catalog        |          Partial          | characters can be accepted, when only       | 
|                                   |                           | numbers of exactly 13 digits should be      | 
|                                   |                           | accepted, as specified in R1.               | 
|                                   |                           |                                             | 
|                                   |                           | Note: All the points below will make the    | 
|                                   |                           | add_book page return with an error, but     | 
|                                   |                           | add_book_to_catalog will return false as    | 
|                                   |                           | it should, so they do not violate R1.       | 
|                                   |                           |                                             | 
|                                   |                           | The ISBN number field produces an error on  |
|                                   |                           | the website if you try to submit a book     |
|                                   |                           |  with only 1-12 digits in the field.        | 
|                                   |                           |                                             | 
|                                   |                           | The Total Copies field produces an error on |
|                                   |                           | the website if you try to submit with a     | 
|                                   |                           | floating point number with a fractional     | 
|                                   |                           | part of 0 (ex. 1.0, 5.0, etc).              |  
|                                   |                           |                                             |
|                                   |                           | The Total Copies field will produce a       | 
|                                   |                           | database error on the website if you try    | 
|                                   |                           | to submit with a very large integer value   |    
|                                   |                           | (since there is no limit to how large the   |  
|                                   |                           | number can be).                             |
|-----------------------------------|---------------------------|---------------------------------------------|
|       borrow_book_by_patron       |          Partial          | A single patron (using the same patron ID)  | 
|                                   |                           | is able to borrow a maximum of 6 books,     | 
|                                   |                           | when the borrowing limit should be 5 books  | 
|                                   |                           | according to R3.                            |
|-----------------------------------|---------------------------|---------------------------------------------|
|       return_book_by_patron       |    Not Yet Implemented    | Book return functionality not yet           |
|                                   |                           | implemented.                                |
|-----------------------------------|---------------------------|---------------------------------------------|
|    calculate_late_fee_for_book    |    Not Yet Implemented    | Late fee calculation functionality not yet  |
|                                   |                           | implemented.                                |
|-----------------------------------|---------------------------|---------------------------------------------|
|      search_books_in_catalog      |    Not Yet Implemented    | Book search functionality not yet           |
|                                   |                           | implemented.                                |
|-----------------------------------|---------------------------|---------------------------------------------|
|      get_patron_status_report     |    Not Yet Implemented    | Patron status report not yet implemented.   |
|-----------------------------------|---------------------------|---------------------------------------------|

# Part C:

## General Notes: 
- These scripts were tested outside of the 'tests' folder. To test them, put them into the main folder 
  so it can access other scripts it requires functions from.

- Some test functions were added into the 'database.py' script to assist with testing. Brief descriptions 
  of each function can be found in the 'database.py' script itself.

- A script called 'resetdata.py' was added for testing purposes to more easily reset the database while
  testing. When testing scripts, make sure to run 'python3 resetdata.py' in the terminal before running 
  'pytest' so tests run correctly. (all test scripts will have a warning of this nature as well)


## Test Scripts:

### R1_test.py: 
- Designed to test for R1, mainly testing the library_service.py add_book_to_catalog function.
- Tests valid input, and invalid input with no title, no author, too long of a title, too long of an
  author, a negative value of total copies, and a ISBN number comprised of only characters.

### R2_test.py: 
- Designed to test for R2, mainly testing the database.py get_all_books function.
- Tests valid catalogs with two books, no books and with one book with less available copies 
  than total copies. Also tests for when a book is added and then removed from the catalog.
- Assumes that the add_book_to_catalog function works as intended.

### R3_test.py: 
- Designed to test for R3, mainly testing the library_service.py borrow_book_by_patron function.
- Tests for valid input, and invalid input with no patron id, no book id, attempting to borrow a book 
  without any copies left, and attempting to borrow more books than the borrow limit.
- Assumes that the add_book_to_catalog function works as intended.

### R4_test.py: 
- Designed to test for R4, mainly testing the library_service.py return_book_by_patron function.
- Tests for valid input, and invalid input with no patron id, no book id, and attempting to return without
  having borrowed a book first.
- Assumes that the add_book_to_catalog and borrow_book_by_patron functions work as intended.

### R5_test.py: 
- Designed to test for R5, mainly testing the library_service.py calculate_late_fee_for_book function.
- Tests for a regular valid calculation, a valid calculuation with a resulting maximum fee, and invalid input
  with no patron id and no book id.
- Assumes that if calculate_late_fee_for_book should return 'false', 'fee_amount' and 'days_overdue' will be 
  set to -1 (more details are in the script itself).

### R6_test.py: 
- Designed to test for R6, mainly testing the library_service.py search_books_in_catalog function.
- Tests for successful searches of a partically matched title, partially matched author and exact matched
  ISBN. Also tests invalid input with an invalid ISBN and an invalid search method. 
- Assumes that the add_book_to_catalog and borrow_book_by_patron functions work as intended.

### R7_test.py: 
- Designed to test for R7, mainly testing the library_service.py get_patron_status_report function.
- Tests for valid patron records consisting of no books, one book and two books. Also tests invalid input with
  an invalid patron id.
- Heavy assumptions were made about what get_patron_status_report should return. More details about these
  assumptions are detailed in the script itself.
