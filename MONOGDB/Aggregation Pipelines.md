# **Aggregation Pipelines**

## **1. Filtering and Matching Stages**

### **$match**
- **Description:**  
  Filters documents in the pipeline to only those that match the specified criteria. It’s analogous to a query’s WHERE clause.
- **When to Use:**  
  Use at the beginning of your pipeline to limit documents for later stages and improve performance.
- **Syntax:**  
  ```js
  { $match: { field: condition } }
  ```
- **Example:**
  ```js
  db.collection.aggregate([
    { $match: { status: "active", age: { $gte: 18 } } }
  ]);
  ```
  
---

## **2. Document Transformation Stages**

### **$project**
- **Description:**  
  Selects, includes, excludes, renames, or computes new fields. It reshapes each document.
- **When to Use:**  
  Use to limit output fields or to compute new fields for subsequent stages.
- **Syntax:**  
  ```js
  { $project: { field1: 1, field2: 1, computedField: { $add: ["$num1", "$num2"] } } }
  ```
- **Example:**
  ```js
  db.collection.aggregate([
    { $project: { _id: 0, name: 1, finalPrice: { $subtract: ["$price", "$discount"] } } }
  ]);
  ```

### **$addFields / $set**
- **Description:**  
  Adds new fields or overrides existing ones in each document.  
  (Note: `$set` is an alias for `$addFields`.)
- **When to Use:**  
  Use when you need to enrich documents with computed or static values without removing other fields.
- **Syntax:**  
  ```js
  { $addFields: { newField: "value", computedField: { $multiply: ["$quantity", "$price"] } } }
  ```
- **Example:**
  ```js
  db.collection.aggregate([
    {
      $addFields: {
        totalCost: { $multiply: ["$price", "$quantity"] },
        currency: "USD"
      }
    }
  ]);
  ```

### **$unset**
- **Description:**  
  Removes specified fields from documents.
- **When to Use:**  
  Use after transformations if you want to remove sensitive or unnecessary fields before sending data to clients.
- **Syntax:**  
  ```js
  { $unset: "fieldName" }
  ```
- **Example:**
  ```js
  db.collection.aggregate([
    { $unset: "temporaryField" }
  ]);
  ```

### **$replaceRoot / $replaceWith**
- **Description:**  
  Replaces the entire document with the specified document.  
  `$replaceWith` is the newer alias.
- **When to Use:**  
  Use to change the document’s root—often after joining data or when restructuring nested documents.
- **Syntax:**  
  ```js
  { $replaceWith: { newField: "$oldField", otherField: "$anotherField" } }
  ```
- **Example:**
  ```js
  db.collection.aggregate([
    { $replaceWith: { name: "$title", price: "$cost" } }
  ]);
  ```

---

## **3. Grouping and Aggregating Stages**

### **$group**
- **Description:**  
  Groups documents based on a key and performs aggregate computations (like sum, avg, etc.) for each group.
- **When to Use:**  
  Use when you need to summarize data—such as total sales per category or count per user.
- **Syntax:**  
  ```js
  {
    $group: {
      _id: "$groupField",
      total: { $sum: "$amount" },
      avgValue: { $avg: "$value" }
    }
  }
  ```
- **Example:**
  ```js
  db.sales.aggregate([
    {
      $group: {
        _id: "$productId",
        totalSales: { $sum: { $multiply: ["$price", "$quantity"] } },
        count: { $sum: 1 }
      }
    }
  ]);
  ```

### **$bucket**
- **Description:**  
  Divides documents into buckets based on specified boundaries (like histogram bins).
- **When to Use:**  
  Use when you want to categorize numeric data into ranges.
- **Syntax:**  
  ```js
  {
    $bucket: {
      groupBy: "$price",
      boundaries: [0, 100, 200, 300, 400],
      default: "Other",
      output: { count: { $sum: 1 } }
    }
  }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    {
      $bucket: {
        groupBy: "$price",
        boundaries: [0, 100, 200, 300, 400],
        default: "Other",
        output: { count: { $sum: 1 }, avgPrice: { $avg: "$price" } }
      }
    }
  ]);
  ```

### **$bucketAuto**
- **Description:**  
  Automatically divides documents into a specified number of buckets with approximately equal counts.
- **When to Use:**  
  Use when you prefer the database to determine the optimal bucket boundaries.
- **Syntax:**  
  ```js
  {
    $bucketAuto: {
      groupBy: "$price",
      buckets: 4,
      output: { count: { $sum: 1 }, avgPrice: { $avg: "$price" } }
    }
  }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    {
      $bucketAuto: {
        groupBy: "$price",
        buckets: 4,
        output: { count: { $sum: 1 }, avgPrice: { $avg: "$price" } }
      }
    }
  ]);
  ```

### **$sortByCount**
- **Description:**  
  Groups documents by a specified expression and then counts the number of documents in each group, sorting by count.
- **When to Use:**  
  Useful for quickly summarizing the frequency of occurrences.
- **Syntax:**  
  ```js
  { $sortByCount: "$field" }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $sortByCount: "$category" }
  ]);
  ```

### **$count**
- **Description:**  
  Counts the number of documents that pass through the pipeline and outputs a document with the count.
- **When to Use:**  
  Use at the end of a pipeline when you simply need a document count.
- **Syntax:**  
  ```js
  { $count: "totalDocuments" }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $match: { category: "Electronics" } },
    { $count: "numElectronics" }
  ]);
  ```

---

## **4. Data Ordering and Pagination Stages**

### **$sort**
- **Description:**  
  Sorts documents based on specified fields, either ascending (1) or descending (-1).
- **When to Use:**  
  Use after filtering/grouping to order your data.  
  Optimized if fields are indexed.
- **Syntax:**  
  ```js
  { $sort: { field1: 1, field2: -1 } }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $sort: { price: -1, rating: 1 } }
  ]);
  ```

### **$limit**
- **Description:**  
  Restricts the pipeline to pass a specified number of documents.
- **When to Use:**  
  Use to control output size—for example, the top N results.
- **Syntax:**  
  ```js
  { $limit: <number> }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $sort: { price: 1 } },
    { $limit: 5 }
  ]);
  ```

### **$skip**
- **Description:**  
  Skips over a specified number of documents (commonly used for pagination).
- **When to Use:**  
  Use in combination with `$limit` for paginated output.
- **Syntax:**  
  ```js
  { $skip: <number> }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $sort: { price: 1 } },
    { $skip: 5 },
    { $limit: 5 }
  ]);
  ```

---

## **5. Array Processing Stages**

### **$unwind**
- **Description:**  
  Deconstructs an array field from the input document to output a document for each element.
- **When to Use:**  
  Use when you need to process or filter individual elements of an array.
- **Syntax:**  
  ```js
  { $unwind: "$arrayField" }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $unwind: "$tags" },
    { $match: { tags: "portable" } }
  ]);
  ```

---

## **6. Data Combination and Join Stages**

### **$lookup**
- **Description:**  
  Performs a left outer join to another collection, adding the joined documents as an array.
- **When to Use:**  
  Use when you need to incorporate related data from different collections.
- **Syntax:**  
  ```js
  {
    $lookup: {
      from: "foreignCollection",
      localField: "fieldLocal",
      foreignField: "fieldForeign",
      as: "resultField"
    }
  }
  ```
- **Example:**
  ```js
  db.orders.aggregate([
    {
      $lookup: {
        from: "customers",
        localField: "customerId",
        foreignField: "_id",
        as: "customerDetails"
      }
    }
  ]);
  ```

### **$graphLookup**
- **Description:**  
  Performs recursive search on a collection; useful for hierarchical data.
- **When to Use:**  
  Use when you need to traverse relationships in documents (e.g., organizational charts, category trees).
- **Syntax:**  
  ```js
  {
    $graphLookup: {
      from: "collection",
      startWith: "$field",
      connectFromField: "field",
      connectToField: "field",
      as: "result"
    }
  }
  ```
- **Example:**
  ```js
  db.employees.aggregate([
    {
      $graphLookup: {
        from: "employees",
        startWith: "$managerId",
        connectFromField: "managerId",
        connectToField: "_id",
        as: "managementChain"
      }
    }
  ]);
  ```

### **$unionWith**
- **Description:**  
  Merges pipeline results from the current collection with those from another collection.
- **When to Use:**  
  Use when you need to combine data from multiple collections into one result set.
- **Syntax:**  
  ```js
  { $unionWith: "otherCollection" }
  ```
- **Example:**
  ```js
  db.orders.aggregate([
    { $match: { status: "pending" } },
    { $unionWith: "backorders" },
    { $match: { priority: "high" } }
  ]);
  ```

---

## **7. Parallel Pipeline and Sampling Stages**

### **$facet**
- **Description:**  
  Runs multiple aggregation pipelines in parallel on the same input and returns a document that combines the output of each pipeline.
- **When to Use:**  
  Use when you need to perform different aggregations on the same set of documents concurrently.
- **Syntax:**  
  ```js
  {
    $facet: {
      pipeline1: [ /* stages */ ],
      pipeline2: [ /* stages */ ]
    }
  }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    {
      $facet: {
        byCategory: [
          { $group: { _id: "$category", count: { $sum: 1 } } },
          { $sort: { count: -1 } }
        ],
        priceStats: [
          { $group: { _id: null, avgPrice: { $avg: "$price" }, total: { $sum: 1 } } }
        ]
      }
    }
  ]);
  ```

### **$sample**
- **Description:**  
  Randomly selects the specified number of documents from the input.
- **When to Use:**  
  Use to generate random samples—for example, in A/B testing or random data previews.
- **Syntax:**  
  ```js
  { $sample: { size: <number> } }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $sample: { size: 5 } }
  ]);
  ```

---

## **8. Advanced Analytics and Window Functions**

### **$setWindowFields**
- **Description:**  
  Introduces window functions (similar to SQL window functions) to compute values over a partition of documents.
- **When to Use:**  
  Use when you need cumulative sums, moving averages, or ranking over a sorted partition.
- **Syntax:**  
  ```js
  {
    $setWindowFields: {
      partitionBy: "$groupField",
      sortBy: { sortField: 1 },
      output: {
        runningTotal: {
          $sum: "$value",
          window: { documents: ["unbounded", "current"] }
        }
      }
    }
  }
  ```
- **Example:**
  ```js
  db.sales.aggregate([
    {
      $setWindowFields: {
        partitionBy: "$category",
        sortBy: { date: 1 },
        output: {
          runningTotal: {
            $sum: "$amount",
            window: { documents: ["unbounded", "current"] }
          }
        }
      }
    }
  ]);
  ```

---

## **9. Geospatial and Collection Statistics**

### **$geoNear**
- **Description:**  
  Performs a geospatial query, adding a calculated distance field. Must be the first stage.
- **When to Use:**  
  Use when querying documents by proximity to a point.
- **Syntax:**  
  ```js
  {
    $geoNear: {
      near: { type: "Point", coordinates: [ <longitude>, <latitude> ] },
      distanceField: "distance",
      maxDistance: <distance>,
      spherical: true
    }
  }
  ```
- **Example:**
  ```js
  db.places.aggregate([
    {
      $geoNear: {
        near: { type: "Point", coordinates: [ -73.99279, 40.719296 ] },
        distanceField: "distance",
        maxDistance: 1000,
        spherical: true
      }
    }
  ]);
  ```

### **$collStats**
- **Description:**  
  Retrieves statistics about the collection such as latency or document count distribution.
- **When to Use:**  
  Use for debugging or to monitor collection performance.
- **Syntax:**  
  ```js
  { $collStats: { latencyStats: { } } }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $collStats: { latencyStats: { } } }
  ]);
  ```

### **$indexStats**
- **Description:**  
  Provides statistics about index usage on a collection.
- **When to Use:**  
  Use for monitoring index performance and diagnosing query issues.
- **Syntax:**  
  ```js
  { $indexStats: { } }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $indexStats: { } }
  ]);
  ```

---

## **10. Security and Debugging**

### **$redact**
- **Description:**  
  Applies document-level access control by evaluating and conditionally including/excluding document sections.
- **When to Use:**  
  Use to enforce field-level security rules based on custom logic.
- **Syntax:**  
  ```js
  {
    $redact: {
      $cond: {
        if: { <expression> },
        then: "$$DESCEND",  // continue processing document
        else: "$$PRUNE"     // remove document
      }
    }
  }
  ```
- **Example:**
  ```js
  db.documents.aggregate([
    {
      $redact: {
        $cond: {
          if: { $eq: ["$classification", "public"] },
          then: "$$DESCEND",
          else: "$$PRUNE"
        }
      }
    }
  ]);
  ```

### **$planCacheStats**
- **Description:**  
  Provides information about the aggregation plan cache, useful for debugging or performance analysis.
- **When to Use:**  
  Rarely used in a production pipeline; generally for monitoring how aggregation plans are being reused.
- **Syntax:**  
  ```js
  { $planCacheStats: { } }
  ```
- **Example:**
  ```js
  db.products.aggregate([
    { $planCacheStats: { } }
  ]);
  ```

---

## **11. Output Stages**

### **$merge**
- **Description:**  
  Writes the results of the aggregation pipeline into an existing collection, updating or inserting documents based on specified conditions.
- **When to Use:**  
  Use when you want the processed data to be persisted in a collection.
- **Syntax:**  
  ```js
  {
    $merge: {
      into: "targetCollection",
      on: "_id", // field(s) for matching
      whenMatched: "replace", // or "merge", "keepExisting", etc.
      whenNotMatched: "insert"
    }
  }
  ```
- **Example:**
  ```js
  db.sales.aggregate([
    { $group: { _id: "$productId", totalSales: { $sum: "$amount" } } },
    {
      $merge: {
        into: "salesSummary",
        on: "_id",
        whenMatched: "merge",
        whenNotMatched: "insert"
      }
    }
  ]);
  ```

### **$out**
- **Description:**  
  Writes the output of the aggregation pipeline to a new collection. This stage overwrites the collection if it already exists.
- **When to Use:**  
  Use when you need to persist an entire pipeline result as a new collection for reporting or further analysis.
- **Syntax:**  
  ```js
  { $out: "newCollectionName" }
  ```
- **Example:**
  ```js
  db.sales.aggregate([
    { $match: { status: "completed" } },
    { $group: { _id: "$productId", count: { $sum: 1 } } },
    { $out: "completedSales" }
  ]);
  ```

---

## **Summary Table**

| Stage                | Description                                                 | When to Use                                                     | Example (Node.js Syntax)                                              |
|----------------------|-------------------------------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------|
| **$match**           | Filters documents                                           | Early stage filtering                                           | `{ $match: { status: "active" } }`                                     |
| **$project**         | Reshapes documents (include/exclude/compute fields)         | Controlling output fields                                       | `{ $project: { name: 1, price: 1 } }`                                   |
| **$addFields / $set** | Adds or overwrites fields                                   | Enriching documents                                             | `{ $addFields: { total: { $multiply: [ "$price", "$qty" ] } } }`        |
| **$unset**           | Removes fields                                              | Cleaning up output                                              | `{ $unset: "internalField" }`                                          |
| **$replaceWith**     | Replaces the whole document                                 | Re-rooting documents                                            | `{ $replaceWith: { newName: "$oldField" } }`                            |
| **$group**           | Groups documents and aggregates data                        | Summarizing data (e.g., totals, averages)                         | `{ $group: { _id: "$category", total: { $sum: "$price" } } }`           |
| **$bucket**          | Groups documents into user-defined ranges                   | Creating histograms                                             | `{ $bucket: { groupBy: "$price", boundaries: [0,100,200], default: "Other" } }` |
| **$bucketAuto**      | Automatically groups documents into buckets                 | When you prefer MongoDB to decide bucket boundaries               | `{ $bucketAuto: { groupBy: "$price", buckets: 4 } }`                     |
| **$sortByCount**     | Groups and counts occurrences, then sorts                   | Quick frequency analysis                                          | `{ $sortByCount: "$category" }`                                        |
| **$count**           | Counts documents                                            | When only total count is needed                                   | `{ $count: "totalDocs" }`                                              |
| **$sort**            | Orders documents                                            | Final sorting, pagination                                        | `{ $sort: { price: -1 } }`                                             |
| **$limit**           | Limits output documents                                     | Controlling output size                                           | `{ $limit: 10 }`                                                      |
| **$skip**            | Skips documents                                             | Pagination                                                       | `{ $skip: 20 }`                                                       |
| **$unwind**          | Deconstructs an array field into multiple documents         | When processing elements of an array individually                 | `{ $unwind: "$tags" }`                                                 |
| **$lookup**          | Joins data from another collection                          | Combining related documents from separate collections              | `{ $lookup: { from: "customers", localField: "cid", foreignField: "_id", as: "cust" } }` |
| **$graphLookup**     | Recursively searches documents                              | Hierarchical data (e.g., organizational trees)                     | `{ $graphLookup: { from: "employees", startWith: "$managerId", connectFromField: "managerId", connectToField: "_id", as: "chain" } }` |
| **$unionWith**       | Unions pipelines from two collections                        | Combining similar data from different collections                  | `{ $unionWith: "otherCollection" }`                                    |
| **$facet**           | Runs multiple pipelines in parallel                         | When multiple aggregations are needed in one query                    | `{ $facet: { stage1: [ ... ], stage2: [ ... ] } }`                      |
| **$sample**          | Returns a random sample of documents                         | Random sampling for A/B tests or previews                             | `{ $sample: { size: 5 } }`                                               |
| **$setWindowFields** | Applies window functions to compute cumulative or moving totals | Advanced analytics (e.g., running totals, ranks)                      | `{ $setWindowFields: { partitionBy: "$category", sortBy: { date: 1 }, output: { runningTotal: { $sum: "$amount", window: { documents: [ "unbounded", "current" ] } } } } }` |
| **$geoNear**         | Performs a geospatial query and calculates distances          | Location-based searches (must be first stage)                          | `{ $geoNear: { near: { type: "Point", coordinates: [ -73.99, 40.73 ] }, distanceField: "dist", spherical: true } }` |
| **$collStats**       | Outputs collection-level statistics                           | Monitoring and diagnostics                                           | `{ $collStats: { latencyStats: {} } }`                                  |
| **$indexStats**      | Outputs index usage statistics                                | Optimizing queries                                                   | `{ $indexStats: {} }`                                                  |
| **$redact**          | Enforces document-level access control                        | Security filtering based on content                                  | `{ $redact: { $cond: { if: { $eq: ["$classification", "public"] }, then: "$$DESCEND", else: "$$PRUNE" } } }` |
| **$planCacheStats**  | Returns stats on aggregation plan caches                      | Debugging performance issues                                         | `{ $planCacheStats: {} }`                                              |
| **$merge**           | Merges the results into an existing collection                | Persisting aggregation output (update/insert)                         | `{ $merge: { into: "target", on: "_id", whenMatched: "merge", whenNotMatched: "insert" } }` |
| **$out**             | Outputs the aggregation result to a new collection              | Persisting complete aggregation results as a new collection            | `{ $out: "newCollectionName" }`                                        |

---

## **Usage Conditions and Considerations**

- **Indexing:**  
  Use indexes with `$match` and `$sort` to optimize performance.

- **Pipeline Order:**  
  Place filtering (`$match`) early; transformation (`$project`, `$addFields`) and grouping (`$group`) come next. Output stages like `$merge` and `$out` should be at the end.

- **Memory & Performance:**  
  Stages like `$group` and `$facet` may require more memory; use them judiciously with large collections. Consider using `$sample` early if you only need a subset.

- **Transactional Changes:**  
  When outputting results with `$merge` or `$out`, ensure that concurrent writes or additional processing are managed carefully.

- **Security:**  
  `$redact` can help enforce document-level security. Use it when you need to filter out sensitive data based on custom rules.

---