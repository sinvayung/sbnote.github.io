# 字符串操作函数大全

#### cstring - Copying:

- [**memcpy**](http://www.cplusplus.com/reference/cstring/memcpy/)

  Copy block of memory (function )

  ```c
  void * memcpy ( void * destination, const void * source, size_t num );
  ```

- [**memmove**](http://www.cplusplus.com/reference/cstring/memmove/)

  Move block of memory (function )

  ```c
  void * memmove ( void * destination, const void * source, size_t num );
  ```

- [**strcpy**](http://www.cplusplus.com/reference/cstring/strcpy/)

  Copy string (function )

  ```c
  char * strcpy ( char * destination, const char * source );
  ```

- [**strncpy**](http://www.cplusplus.com/reference/cstring/strncpy/)

  Copy characters from string (function )

  ```c
  char * strncpy ( char * destination, const char * source, size_t num );
  ```

#### cstring - Concatenation:

- [**strcat**](http://www.cplusplus.com/reference/cstring/strcat/)

  Concatenate strings (function )

  ```c
  char * strcat ( char * destination, const char * source );
  ```

- [**strncat**](http://www.cplusplus.com/reference/cstring/strncat/)

  Append characters from string (function )

  ```c
  char * strncat ( char * destination, const char * source, size_t num );
  ```

#### cstring - Comparison:

- [**memcmp**](http://www.cplusplus.com/reference/cstring/memcmp/)

  Compare two blocks of memory (function )

  ```c
  int memcmp ( const void * ptr1, const void * ptr2, size_t num );
  ```

- [**strcmp**](http://www.cplusplus.com/reference/cstring/strcmp/)

  Compare two strings (function )

  ```c
  int strcmp ( const char * str1, const char * str2 );
  ```

- [**strcoll**](http://www.cplusplus.com/reference/cstring/strcoll/)

  Compare two strings using locale (function )

  ```c
  int strcoll ( const char * str1, const char * str2 );
  ```

- [**strncmp**](http://www.cplusplus.com/reference/cstring/strncmp/)

  Compare characters of two strings (function )

  ```c
  int strncmp ( const char * str1, const char * str2, size_t num );
  ```

- [**strxfrm**](http://www.cplusplus.com/reference/cstring/strxfrm/)

  Transform string using locale (function )

  ```c
  size_t strxfrm ( char * destination, const char * source, size_t num );
  ```

#### cstring - Searching:

- [**memchr**](http://www.cplusplus.com/reference/cstring/memchr/)

  Locate character in block of memory (function )

  ```c
  const void * memchr ( const void * ptr, int value, size_t num );
        void * memchr (       void * ptr, int value, size_t num );
  ```

- [**strchr**](http://www.cplusplus.com/reference/cstring/strchr/)

  Locate first occurrence of character in string (function )

  ```c
  const char * strchr ( const char * str, int character );
        char * strchr (       char * str, int character );
  ```

- [**strcspn**](http://www.cplusplus.com/reference/cstring/strcspn/)

  Get span until character in string (function )

  ```c
  size_t strcspn ( const char * str1, const char * str2 );
  ```

- [**strpbrk**](http://www.cplusplus.com/reference/cstring/strpbrk/)

  Locate characters in string (function )

  ```c
  const char * strpbrk ( const char * str1, const char * str2 );
        char * strpbrk (       char * str1, const char * str2 );
  ```

- [**strrchr**](http://www.cplusplus.com/reference/cstring/strrchr/)

  Locate last occurrence of character in string (function )

  ```c
  const char * strrchr ( const char * str, int character );
        char * strrchr (       char * str, int character );
  ```

- [**strspn**](http://www.cplusplus.com/reference/cstring/strspn/)

  Get span of character set in string (function )

  ```c
  size_t strspn ( const char * str1, const char * str2 );
  ```

- [**strstr**](http://www.cplusplus.com/reference/cstring/strstr/)

  Locate substring (function )

  ```c
  const char * strstr ( const char * str1, const char * str2 );
        char * strstr (       char * str1, const char * str2 );
  ```

- [**strtok**](http://www.cplusplus.com/reference/cstring/strtok/)

  Split string into tokens (function )

  ```c
  char * strtok ( char * str, const char * delimiters );
  ```

  Example

  ```c
  #include <stdio.h>
  #include <string.h>
  
  int main ()
  {
    char str[] ="- This, a sample string.";
    char * pch;
    pch = strtok (str," ,.-");
    while (pch != NULL)
    {
      printf ("%s\n",pch);
      pch = strtok (NULL, " ,.-");
    }
    return 0;
  }
  ```

#### cstring - Other:

- [**memset**](http://www.cplusplus.com/reference/cstring/memset/)

  Fill block of memory (function )

  ```c
  void * memset ( void * ptr, int value, size_t num );
  ```

- [**strerror**](http://www.cplusplus.com/reference/cstring/strerror/)

  Get pointer to error message string (function )

  ```c
  char * strerror ( int errnum );
  ```

  Example

  ```c
  #include <stdio.h>
  #include <string.h>
  #include <errno.h>
  
  int main ()
  {
    FILE * pFile;
    pFile = fopen ("unexist.ent","r");
    if (pFile == NULL)
      printf ("Error opening file unexist.ent: %s\n",strerror(errno));
    return 0;
  }
  ```

- [**strlen**](http://www.cplusplus.com/reference/cstring/strlen/)

  Get string length (function )

  ```C
  size_t strlen ( const char * str );
  ```

- [**strdup**](https://linux.die.net/man/3/strdup)

  Duplicate a string (linux)

  ```c
  char *strdup(const char *s);
  char *strndup(const char *s, size_t n);
  char *strdupa(const char *s);
  char *strndupa(const char *s, size_t n);
  ```



#### cstdlib - String conversion:

- [**atof**](http://www.cplusplus.com/reference/cstdlib/atof/)

  Convert string to double (function )

  ```c
  double atof (const char* str);
  ```

- [**atoi**](http://www.cplusplus.com/reference/cstdlib/atoi/)

  Convert string to integer (function )

  ```c
  int atoi (const char * str);
  ```

- [**atol**](http://www.cplusplus.com/reference/cstdlib/atol/)

  Convert string to long integer (function )

  ```c
  long int atol ( const char * str );
  ```

- [**atoll** ](http://www.cplusplus.com/reference/cstdlib/atoll/)

  Convert string to long long integer (function )

- [**strtod**](http://www.cplusplus.com/reference/cstdlib/strtod/)

  Convert string to double (function )

  ```c
  double strtod (const char* str, char** endptr);
  ```

- [**strtof** ](http://www.cplusplus.com/reference/cstdlib/strtof/)

  Convert string to float (function )

- [**strtol**](http://www.cplusplus.com/reference/cstdlib/strtol/)

  Convert string to long integer (function )

  ```c
  long int strtol (const char* str, char** endptr, int base);
  ```

  Example

  ```c
  #include <stdio.h>      /* printf */
  #include <stdlib.h>     /* strtol */
  
  int main ()
  {
    char szNumbers[] = "2001 60c0c0 -1101110100110100100000 0x6fffff";
    char * pEnd;
    long int li1, li2, li3, li4;
    li1 = strtol (szNumbers,&pEnd,10);
    li2 = strtol (pEnd,&pEnd,16);
    li3 = strtol (pEnd,&pEnd,2);
    li4 = strtol (pEnd,NULL,0);
    printf ("The decimal equivalents are: %ld, %ld, %ld and %ld.\n", li1, li2, li3, li4);
    return 0;
  }
  ```

- [**strtold** ](http://www.cplusplus.com/reference/cstdlib/strtold/)

  Convert string to long double (function )

- [**strtoll** ](http://www.cplusplus.com/reference/cstdlib/strtoll/)

  Convert string to long long integer (function )

- [**strtoul**](http://www.cplusplus.com/reference/cstdlib/strtoul/)

  Convert string to unsigned long integer (function )

  ```c
  unsigned long int strtoul (const char* str, char** endptr, int base);
  ```

- [**strtoull** ](http://www.cplusplus.com/reference/cstdlib/strtoull/)

  Convert string to unsigned long long integer (function )



#### cstdio - Formatted input/output:

- [**snprintf** ](http://www.cplusplus.com/reference/cstdio/snprintf/)

  Write formatted output to sized buffer (function )

- [**sprintf**](http://www.cplusplus.com/reference/cstdio/sprintf/)

  Write formatted data to string (function )

  ```c
  int sprintf ( char * str, const char * format, ... );
  ```

- [**sscanf**](http://www.cplusplus.com/reference/cstdio/sscanf/)

  Read formatted data from string (function )

  ```c
  int sscanf ( const char * s, const char * format, ...);
  ```

  Example

  ```c
  #include <stdio.h>
  
  int main ()
  {
    char sentence []="Rudolph is 12 years old";
    char str [20];
    int i;
  
    sscanf (sentence,"%s %*s %d",str,&i);
    printf ("%s -> %d\n",str,i);
    
    return 0;
  }
  ```

- [**vsnprintf** ](http://www.cplusplus.com/reference/cstdio/vsnprintf/)

  Write formatted data from variable argument list to sized buffer (function )

- [**vsprintf**](http://www.cplusplus.com/reference/cstdio/vsprintf/)

  Write formatted data from variable argument list to string (function )

  ```c
  int vsprintf (char * s, const char * format, va_list arg );
  ```

- [**vsscanf** ](http://www.cplusplus.com/reference/cstdio/vsscanf/)

  Read formatted data from string into variable argument list (function )