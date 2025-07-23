# **5. Aggregation Operators:**

## **1. Arithmetic Operators**

These operators perform numerical calculations.

- **`$add`**  
  *Description:* Adds numbers, dates, or arrays (concatenating arrays).  
  *Use Cases:* Calculating totals, sums, or concatenating arrays.  
  *Syntax:*  
  ```js
  { $add: [ expression1, expression2, ... ] }
  ```
  *Example (Aggregation):*  
  ```js
  // Calculate final price
  db.sales.aggregate([
    { $project: { finalPrice: { $add: [ "$price", "$tax" ] } } }
  ]);
  ```  
  *Usage in Updates:*  
  Within an update pipeline you can use `$add` in a `$set` stage to compute new field values.

- **`$subtract`**  
  *Description:* Subtracts one value from another.  
  *Example:*  
  ```js
  { $subtract: [ "$price", "$discount" ] }
  ```

- **`$multiply`**  
  *Description:* Multiplies numbers.  
  *Example:*  
  ```js
  { $multiply: [ "$price", "$quantity" ] }
  ```

- **`$divide`**  
  *Description:* Divides one number by another.  
  *Example:*  
  ```js
  { $divide: [ "$total", "$count" ] }
  ```

- **`$mod`**  
  *Description:* Returns the remainder after dividing one number by another.  
  *Example:*  
  ```js
  { $mod: [ "$age", 5 ] }  // Useful for cyclic grouping (e.g. divisible by 5)
  ```

- **Other Math Operators:**  
  - **`$abs`**: Absolute value  
    ```js
    { $abs: "$value" }
    ```
  - **`$ceil`**: Rounds up  
    ```js
    { $ceil: "$value" }
    ```
  - **`$floor`**: Rounds down  
    ```js
    { $floor: "$value" }
    ```
  - **`$trunc`**: Truncates to an integer  
    ```js
    { $trunc: "$value" }
    ```

*Note:* These arithmetic operators work inside aggregation expressions (such as in `$project` or in an update pipeline with `$set`). They are not used directly in standard find queries unless wrapped in `$expr`.

---

## **2. Comparison Operators**

These operators compare values and return a Boolean result (or an integer in the case of `$cmp`).

- **`$eq`**  
  *Description:* Returns true if the values are equal.  
  *Example:*  
  ```js
  { $eq: [ "$field", 100 ] }
  ```

- **`$ne`**  
  *Description:* Returns true if values are not equal.  
  *Example:*  
  ```js
  { $ne: [ "$status", "inactive" ] }
  ```

- **`$gt`**, **`$gte`**, **`$lt`**, **`$lte`**  
  *Description:* Greater than, greater than or equal, less than, and less than or equal.  
  *Example:*  
  ```js
  { $gt: [ "$age", 18 ] }
  ```

- **`$cmp`**  
  *Description:* Compares two values and returns -1, 0, or 1.  
  *Example:*  
  ```js
  { $cmp: [ "$value1", "$value2" ] }
  ```

*Usage:* These are often used inside `$match` with `$expr` or within `$project` to create computed Boolean fields. They also work in update pipelines if you need conditional logic (combined with `$cond`).

---

## **3. Logical Operators**

Evaluate Boolean logic across expressions.

- **`$and`**  
  *Description:* Returns true if all expressions are true.  
  *Example:*  
  ```js
  { $and: [ { $gt: [ "$age", 18 ] }, { $lt: [ "$age", 65 ] } ] }
  ```

- **`$or`**  
  *Description:* Returns true if any expression is true.  
  *Example:*  
  ```js
  { $or: [ { $eq: [ "$status", "A" ] }, { $eq: [ "$status", "B" ] } ] }
  ```

- **`$not`**  
  *Description:* Inverts the result of an expression.  
  *Example:*  
  ```js
  { $not: { $eq: [ "$status", "inactive" ] } }
  ```

*Usage:* Logical operators are used within aggregation expressions and within `$expr` queries. They are not directly applied in update operators unless within an aggregation update.

---

## **4. Conditional Operators**

Provide if/then/else logic.

- **`$cond`**  
  *Description:* Ternary operator: evaluates a condition and returns one value if true and another if false.  
  *Syntax:*  
  ```js
  { $cond: { if: <boolean-expression>, then: <true-case>, else: <false-case> } }
  ```
  *Example:*  
  ```js
  {
    $project: {
      statusText: {
        $cond: { if: { $gte: [ "$score", 70 ] }, then: "Pass", else: "Fail" }
      }
    }
  }
  ```

- **`$ifNull`**  
  *Description:* Returns a specified value if the expression resolves to null.  
  *Example:*  
  ```js
  { $ifNull: [ "$field", "defaultValue" ] }
  ```

- **`$switch`**  
  *Description:* Evaluates a series of case expressions and returns the first matching result.  
  *Syntax:*  
  ```js
  {
    $switch: {
      branches: [
        { case: <expression1>, then: <result1> },
        { case: <expression2>, then: <result2> }
      ],
      default: <default-result>
    }
  }
  ```
  *Example:*  
  ```js
  {
    $project: {
      grade: {
        $switch: {
          branches: [
            { case: { $gte: [ "$score", 90 ] }, then: "A" },
            { case: { $gte: [ "$score", 80 ] }, then: "B" }
          ],
          default: "C"
        }
      }
    }
  }
  ```

*Usage:* These conditional operators are extensively used in `$project` stages to derive new fields. They can also be used inside update pipelines (using the aggregation pipeline form) and within `$expr` in find queries.

---

## **5. Array Operators**

Designed for processing array data.

- **`$arrayElemAt`**  
  *Description:* Returns the element at the specified array index.  
  *Example:*  
  ```js
  { $arrayElemAt: [ "$tags", 0 ] }
  ```

- **`$concatArrays`**  
  *Description:* Concatenates arrays.  
  *Example:*  
  ```js
  { $concatArrays: [ "$arr1", "$arr2" ] }
  ```

- **`$filter`**  
  *Description:* Selects a subset of an array to return based on a condition.  
  *Syntax:*  
  ```js
  {
    $filter: {
      input: "$array",
      as: "item",
      cond: { $gt: [ "$$item.score", 50 ] }
    }
  }
  ```
- **`$isArray`**  
  *Description:* Returns a Boolean indicating whether the argument is an array.  
  *Example:*  
  ```js
  { $isArray: "$tags" }
  ```

- **`$size`**  
  *Description:* Returns the size (i.e., the number of elements) of an array.  
  *Example:*  
  ```js
  { $size: "$arrayField" }
  ```

- **`$slice`**  
  *Description:* Returns a subset of an array.  
  *Example:*  
  ```js
  { $slice: [ "$arrayField", 0, 3 ] }
  ```

- **`$first`** and **`$last`**  
  *Description:* Return the first or last element of an array (used mainly within group accumulators).  
  *Example:*  
  ```js
  { $first: "$arrayField" }
  ```

- **`$indexOfArray`**  
  *Description:* Returns the index of a specified element in an array.  
  *Example:*  
  ```js
  { $indexOfArray: [ "$arrayField", "target" ] }
  ```

*Usage:* Array operators are used within `$project` or `$group` stages to transform or evaluate array fields. In update expressions (with aggregation pipelines), you can use these operators as well.

---

## **6. String Operators**

Operators to manipulate text strings.

- **`$concat`**  
  *Description:* Joins strings together.  
  *Example:*  
  ```js
  { $concat: [ "$firstName", " ", "$lastName" ] }
  ```

- **`$substr`** and **`$substrCP`**  
  *Description:* Returns a substring of a string; `$substrCP` counts code points properly.  
  *Example:*  
  ```js
  { $substr: [ "$field", 0, 5 ] }
  ```

- **`$toLower`** and **`$toUpper`**  
  *Description:* Converts a string to lowercase or uppercase.  
  *Example:*  
  ```js
  { $toLower: "$name" }
  ```

- **`$trim`**, **`$ltrim`**, **`$rtrim`**  
  *Description:* Removes whitespace or specified characters from the beginning and/or end of a string.  
  *Example:*  
  ```js
  { $trim: { input: "$text", chars: " " } }
  ```

- **`$strLenBytes`** and **`$strLenCP`**  
  *Description:* Returns the length of a string in bytes or in UTF-8 code points.  
  *Example:*  
  ```js
  { $strLenCP: "$text" }
  ```

- **`$split`**  
  *Description:* Splits a string into an array of substrings based on a delimiter.  
  *Example:*  
  ```js
  { $split: [ "$fullName", " " ] }
  ```

- **`$strcasecmp`**  
  *Description:* Performs a case-insensitive string comparison; returns 0 if equal.  
  *Example:*  
  ```js
  { $strcasecmp: [ "$name", "vijay" ] }
  ```

*Usage:* String operators are frequently used in `$project` stages to create new string fields or to clean up data. They can also be used in `$expr` for query matching or update computations.

---

## **7. Date Operators**

These operators allow you to format and manipulate date objects.

- **`$dateToString`**  
  *Description:* Converts a date to a string using a specified format.  
  *Example:*  
  ```js
  { $dateToString: { format: "%Y-%m-%d", date: "$createdAt" } }
  ```

- **`$dateFromString`**  
  *Description:* Parses a date string and returns a date object.  
  *Example:*  
  ```js
  { $dateFromString: { dateString: "$dateStr" } }
  ```

- **Individual Date Parts Operators:**  
  - **`$year`**, **`$month`**, **`$dayOfMonth`**, **`$dayOfWeek`**, **`$dayOfYear`**, **`$hour`**, **`$minute`**, **`$second`**, **`$millisecond`**  
    *Usage:* Extract the corresponding part of a date.  
    *Example:*  
    ```js
    { $year: "$createdAt" }
    ```

- **`$dateAdd`** and **`$dateSubtract`**  
  *Description:* Adds or subtracts a specified time interval to/from a date.  
  *Example:*  
  ```js
  { $dateAdd: { startDate: "$createdAt", unit: "day", amount: 5 } }
  ```

*Usage:* Date operators are essential in `$project` or `$group` stages for bucketing or formatting date information. They also work in update operations that use aggregation pipelines.

---

## **8. Set Operators**

Operate on arrays as mathematical sets.

- **`$setEquals`**  
  *Description:* Returns true if two arrays have the same set of elements (ignoring order).  
  *Example:*  
  ```js
  { $setEquals: [ "$array1", "$array2" ] }
  ```

- **`$setIntersection`**  
  *Description:* Returns an array of elements that appear in both input arrays.  
  *Example:*  
  ```js
  { $setIntersection: [ "$array1", "$array2" ] }
  ```

- **`$setUnion`**  
  *Description:* Returns an array that is the union of the input arrays, removing duplicates.  
  *Example:*  
  ```js
  { $setUnion: [ "$array1", "$array2" ] }
  ```

- **`$setDifference`**  
  *Description:* Returns an array with the elements from the first array that do not appear in the second.  
  *Example:*  
  ```js
  { $setDifference: [ "$array1", "$array2" ] }
  ```

- **`$setIsSubset`**  
  *Description:* Checks whether the first array is a subset of the second.
  *Example:*  
  ```js
  { $setIsSubset: [ "$array1", "$array2" ] }
  ```

*Usage:* Set operators are normally used within `$project` or `$group` stages to compare or combine arrays.

---

## **9. Object Operators**

Manipulate objects and convert between objects and arrays.

- **`$mergeObjects`**  
  *Description:* Merges multiple documents/objects into a single document.  
  *Example:*  
  ```js
  { $mergeObjects: [ "$obj1", "$obj2" ] }
  ```
  
- **`$objectToArray`**  
  *Description:* Converts a document (object) to an array of key-value pairs.  
  *Example:*  
  ```js
  { $objectToArray: "$document" }
  ```

- **`$arrayToObject`**  
  *Description:* Converts an array of key-value pairs back into a document.  
  *Example:*  
  ```js
  { $arrayToObject: "$kvPairs" }
  ```

*Usage:* Object operators are useful in transforming document shapes and are available in any aggregation stage that processes document expressions.

---

## **10. Miscellaneous Operators**

- **`$literal`**  
  *Description:* Returns the value without parsing it as an expression. Useful when you want to include a constant as part of your computation.  
  *Example:*  
  ```js
  { $literal: { key: "value" } }
  ```
  
- **`$map`**  
  *Description:* Applies an expression to each element in an array, returning a new array with the transformed elements.  
  *Syntax:*  
  ```js
  {
    $map: {
      input: "$arrayField",
      as: "item",
      in: { $multiply: [ "$$item", 2 ] }
    }
  }
  ```
  
- **`$function`**  
  *Description:* Allows the execution of a user-defined JavaScript function within an aggregation expression. Use with caution due to performance implications.  
  *Example:*  
  ```js
  {
    $function: {
      body: function(x) { return x * 2; },
      args: [ "$value" ],
      lang: "js"
    }
  }
  ```

*Usage:* Both `$literal` and `$map` are common in aggregation pipelines. `$function` is more advanced and generally used only when built-in operators cannot fulfill your logic.

---

## **Context of Use in Queries, Updates, and Aggregation Pipelines**

- **Aggregation Pipelines:**  
  These operators are designed primarily for use within aggregation stages such as `$project`, `$group`, and others. They are the building blocks to compute derived fields, filter data, or manipulate documents.

- **Update Queries with Aggregation Expressions:**  
  Since MongoDB 4.2, you can use aggregation expressions (including many of the above operators) in update statements. For example, using the update pipeline form with `$set`:
  ```js
  db.collection.updateOne(
    { _id: 1 },
    [{
      $set: { updatedScore: { $multiply: [ "$score", 1.1 ] } }
    }]
  );
  ```
  This update uses `$multiply` to compute a new field based on the current score.

- **Find Queries with `$expr`:**  
  Operators can be used in a query with `$expr` to compare fields or compute expressions:
  ```js
  db.collection.find({
    $expr: { $gt: [ "$score", 50 ] }
  });
  ```

- **Standard Queries (findOne, etc.):**  
  Without `$expr`, simple find queries do not evaluate aggregation expressions—they only match static values or use standard query operators (which are similar but not identical to aggregation operators).

---

## **Summary**

Below is a quick reference table (non-exhaustive) of major aggregation operators, their use, and context:

| **Category**   | **Operator**          | **Description**                                          | **Example**                                            | **Context**                            |
|----------------|-----------------------|----------------------------------------------------------|--------------------------------------------------------|----------------------------------------|
| Arithmetic     | `$add`                | Adds values                                              | `{ $add: [ "$a", "$b" ] }`                              | Aggregation, update expressions        |
|                | `$subtract`           | Subtracts values                                         | `{ $subtract: [ "$price", "$discount" ] }`             | Aggregation, update expressions        |
|                | `$multiply`           | Multiplies values                                        | `{ $multiply: [ "$price", "$quantity" ] }`             | Aggregation, update expressions        |
|                | `$divide`             | Divides values                                           | `{ $divide: [ "$total", "$count" ] }`                  | Aggregation, update expressions        |
|                | `$mod`                | Modulus operator                                         | `{ $mod: [ "$age", 5 ] }`                               | Aggregation, update expressions        |
| Comparison     | `$eq`, `$ne`, etc.    | Compare two values                                       | `{ $eq: [ "$field", 100 ] }`                           | Aggregation via `$expr`, `$project`    |
| Logical        | `$and`, `$or`, `$not`  | Logical conditions                                       | `{ $and: [ { $gt: [ "$age", 18 ] }, { $lt: [ "$age", 65 ] } ] }` | Aggregation, `$expr`                   |
| Conditional    | `$cond`               | Ternary condition                                        | `{ $cond: { if: { $gte: [ "$score", 70 ] }, then: "Pass", else: "Fail" } }` | Aggregation, update expressions        |
|                | `$ifNull`             | Returns default if value is null                         | `{ $ifNull: [ "$nickname", "Unknown" ] }`              | Aggregation, update expressions        |
|                | `$switch`             | Multi-case conditional                                   | `{ $switch: { branches: [...], default: "C" } }`       | Aggregation                            |
| Array          | `$arrayElemAt`        | Gets element at index                                    | `{ $arrayElemAt: [ "$tags", 0 ] }`                      | Aggregation, update expressions        |
|                | `$filter`             | Filters an array                                         | ```js { $filter: { input: "$arr", as: "item", cond: { $gt: [ "$$item", 10 ] } } } ``` | Aggregation                        |
|                | `$size`               | Returns the array length                                 | `{ $size: "$tags" }`                                   | Aggregation, update expressions        |
|                | `$concatArrays`       | Concatenates arrays                                      | `{ $concatArrays: [ "$arr1", "$arr2" ] }`              | Aggregation                            |
| String         | `$concat`             | Concatenates strings                                     | `{ $concat: [ "$firstName", " ", "$lastName" ] }`      | Aggregation, update expressions        |
|                | `$toLower` / `$toUpper`| Converts string case                                    | `{ $toLower: "$name" }`                                | Aggregation, update expressions        |
|                | `$trim`, `$ltrim`, `$rtrim` | Trims whitespace or characters                     | `{ $trim: { input: "$text", chars: " " } }`            | Aggregation                            |
|                | `$split`              | Splits a string into an array                            | `{ $split: [ "$fullName", " " ] }`                     | Aggregation                            |
| Date           | `$dateToString`       | Formats a date as a string                               | `{ $dateToString: { format: "%Y-%m-%d", date: "$createdAt" } }` | Aggregation, update expressions        |
|                | `$year`, `$month`, …   | Extracts specific parts from a date                      | `{ $year: "$createdAt" }`                              | Aggregation                            |
| Set            | `$setUnion`           | Unions arrays, removing duplicates                     | `{ $setUnion: [ "$arr1", "$arr2" ] }`                  | Aggregation, update expressions        |
| Object         | `$mergeObjects`       | Merges multiple documents into one                       | `{ $mergeObjects: [ "$doc1", "$doc2" ] }`              | Aggregation, update expressions        |
| Miscellaneous  | `$literal`            | Returns the literal value (prevents evaluation)          | `{ $literal: { key: "value" } }`                       | Aggregation, update expressions        |
|                | `$map`                | Applies an expression to each element in an array         | `{ $map: { input: "$arr", as: "el", in: { $multiply: [ "$$el", 2 ] } } }` | Aggregation   |
|                | `$function`           | Runs a user-defined JavaScript function                   | `{ $function: { body: function(x) { return x * 2; }, args: [ "$value" ], lang: "js" } }` | Aggregation (advanced)         |

---

## **Final Remarks**

- **Where They Run:**  
  Most of these operators are designed for use within the aggregation framework (e.g., inside `$project`, `$group`, `$addFields`, or `$set` in update pipelines). With MongoDB’s support for aggregation in updates (since version 4.2), you can use many of these operators in update pipelines. Standard find queries (like `findOne`) don’t evaluate these expressions unless you wrap them inside `$expr`.

- **Conditions:**  
  Operators are applied to the fields of documents. They are subject to BSON data type rules, and many require that the field exists and is of a compatible type. Always consider indexing fields used in expressions if performance is critical.

- **Examples Provided:**  
  Each example above shows typical usage in the aggregation pipeline. You can run these examples in a Node.js environment with the MongoDB driver by wrapping them in an async function and calling `db.collection.aggregate([...]).toArray()`.