# Wolfram Language ToE Meta-Model
## A 100% Declarative Framework for Wolfram Language Code Structures

A purely declarative meta-model of Wolfram Language code structures—Notebooks, Cells, Expressions, Symbols, Definitions, Contexts, and Packages—expressed under CMCC. No imperative instructions for code transformation; everything is derived from aggregator fields, event/fact references, or constraints.

**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_WolframLang

### Authors

### Abstract
This extension of the CMCC systematically represents Wolfram Language’s core constructs—Notebooks, Cells, Expressions, Symbols, Definitions, and more—under a single Snapshot-Consistent schema. All domain logic, from symbol creation to cell evaluation tracking, is done via aggregator fields, constraints, or event-based facts. No step-by-step imperative instructions are used.

![Wolfram Language ToE Meta-Model Entity Diagram](wolframLang.png)


### Key Points
- Models Wolfram Language structural elements—Notebooks, Cells, Expressions, Symbols, Definitions—declaratively with aggregator formulas, event-based facts, and constraints.
- Eliminates the need for any imperative code to manage or mutate language constructs.
- Demonstrates extensibility to advanced code analytics, symbolic transformations, or usage tracking, all driven by purely factual data references.
- Seamlessly fits into the broader CMCC approach, where logic is declared rather than executed step by step.

### Implications
- Allows a universal environment for capturing Wolfram Language code semantics in a purely fact-based manner.
- Removes the reliance on mutable state transitions—changes in data automatically reflect in aggregator fields (e.g., a new definition for a Symbol immediately updates the Symbol’s definition count).
- Facilitates advanced code analytics—like counting usage of certain symbols, tracking references to external packages, or measuring expression depth—without entangled imperative code.

### Narrative
#### Purely Declarative Wolfram Language Model
In typical code editors, you have to imperatively manipulate cells, definitions, or notebooks. Here, we treat them as factual records, referencing each other via lookups and aggregator fields. For example, a Symbol’s definitions are simply counted by scanning all Definition entities referencing that Symbol—no explicit procedure is needed to 'increase the count'. Any new definition record automatically updates aggregator fields. The entire 'logic of code structure' emerges from the declared data relationships, in line with the CMCC’s goal of no hidden imperative steps.


---

# Schema Overview

## Entity: Notebook

**Description**: A Wolfram Language Notebook—a container holding multiple cells. Purely declarative references to each Cell entity, no imperative commands to add/remove them.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **title**  
  *Type:* scalar, *Datatype:* string  
  
- **kernelSessionId**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **cells**  
  *Target Entity:* Cell, *Type:* one_to_many  
    
  (Join condition: **Cell.notebookId = this.id**)  
  *Description:* Collection of cells belonging to this notebook.

### Aggregations
- **cellCount**  
  *Description:* Number of cells in this notebook.  
  *Formula:* `COUNT(cells)`
- **containsGraphics**  
  *Description:* True if any cell contains at least one Expression with wolframHead='Graphics' or 'Graphics3D'.  
  *Formula:* `EXISTS(cells.expressions WHERE wolframHead IN ['Graphics','Graphics3D'])`
- **containsDynamic**  
  *Description:* True if any Expression with wolframHead='Dynamic' is found in any cell.  
  *Formula:* `EXISTS(cells.expressions WHERE wolframHead='Dynamic')`
- **totalExpressionCount**  
  *Description:* Sum of all expressions across all cells in this notebook.  
  *Formula:* `SUM(cells => expressionCount)`
- **evaluationCount**  
  *Description:* Number of times cells in this notebook have been evaluated (conceptual aggregator referencing evaluation events).  
  *Formula:* `SUM(cells => evaluationCount)`

### Lambdas
- **addCell**
  (Parameters: cell_id)  
  *Formula:* `Cell(cell_id).notebookId == this.id`
- **removeCell**
  (Parameters: cell_id)  
  *Formula:* `Cell(cell_id).notebookId == null`

### Constraints
- **notebookTitleRequired**  
  *Formula:* `title != ''`  
  *Error Message:* Notebook title cannot be empty.

---

## Entity: Cell

**Description**: A cell in a Wolfram Notebook, referencing an optional list of Expressions. Could be input, output, text, etc. All logic is aggregator-based, no imperative updates.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **notebookId**  
  *Type:* lookup, *Datatype:*   
  
- **cellType**  
  *Type:* scalar, *Datatype:* string  
  
- **style**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **expressions**  
  *Target Entity:* Expression, *Type:* one_to_many  
    
  (Join condition: **Expression.cellId = this.id**)  
  *Description:* Expressions that reside in this cell.

### Aggregations
- **expressionCount**  
  *Description:* How many expressions appear in this cell.  
  *Formula:* `COUNT(expressions)`
- **evaluationCount**  
  *Description:* How many times this cell has been evaluated. Conceptual aggregator referencing 'EvaluationEvent' or similar.  
  *Formula:* `COUNT(EvaluationEvent WHERE EvaluationEvent.cellId=this.id)`
- **containsTextOnly**  
  *Description:* True if the cell is purely textual (no expressions or a single text Expression).  
  *Formula:* `(expressionCount=0) OR (ALL(expressions WHERE wolframHead='String'))`

### Lambdas
- **evaluateCell**
    
  *Formula:* `EvaluationEvent(cellId=this.id) => triggers aggregator`
- **addExpression**
  (Parameters: expr_id)  
  *Formula:* `Expression(expr_id).cellId == this.id`


---

## Entity: Expression

**Description**: Represents a symbolic Wolfram Language expression. Tracks its head (e.g., Plus, Times, Graphics), optional textual content, and references.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **cellId**  
  *Type:* lookup, *Datatype:*   
  
- **wolframHead**  
  *Type:* scalar, *Datatype:* string  
  
- **fullFormString**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **subExpressions**  
  *Target Entity:* Expression, *Type:* one_to_many  
    
    
  *Description:* All sub-expressions nested within this expression. Implementation conceptual—could be a separate linking entity.

### Aggregations
- **subExpressionCount**  
  *Description:* How many immediate sub-expressions are nested under this expression.  
  *Formula:* `COUNT(subExpressions)`
- **referencesSymbols**  
  *Description:* Set or list of Symbol IDs referenced within this expression, purely aggregator-based from parse data.  
  *Formula:* `COLLECT(SymbolReference WHERE SymbolReference.expressionId=this.id => symbolId)`
- **containsPattern**  
  *Description:* True if wolframHead is something like 'Pattern','Blank','Condition', etc. Implementation conceptual.  
  *Formula:* `wolframHead IN ['Pattern','Blank','BlankSequence','Condition']`

### Lambdas
- **transformExpression**
  (Parameters: transformationId)  
  *Formula:* `TransformationEvent(expressionId=this.id, transformationId=transformationId)`


---

## Entity: Symbol

**Description**: A named Wolfram Language symbol, living in a specific Context. Can have zero or more definitions (DownValues, UpValues, etc.).

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **symbolName**  
  *Type:* scalar, *Datatype:* string  
  
- **contextId**  
  *Type:* lookup, *Datatype:*   
  

### Lookups
- **definitions**  
  *Target Entity:* Definition, *Type:* one_to_many  
    
  (Join condition: **Definition.symbolId = this.id**)  
  *Description:* All Definition records referencing this symbol.

### Aggregations
- **definitionCount**  
  *Description:* How many distinct definitions (downvalues, upvalues, etc.) are associated with this symbol.  
  *Formula:* `COUNT(definitions)`
- **isSystemSymbol**  
  *Description:* True if contextId corresponds to 'System`'. Implementation conceptual if context is matched by name or ID.  
  *Formula:* `contextId.contextName=='System`'`
- **downValueCount**  
  *Description:* Number of definitions that are specifically downvalues (e.g., 'f[args_]:=rhs'). Implementation conceptual if stored as Definition.defType='DownValue'.  
  *Formula:* `COUNT(definitions WHERE defType='DownValue')`
- **upValueCount**  
  *Description:* Number of definitions that are specifically upvalues (e.g., 'expr^:=rhs').  
  *Formula:* `COUNT(definitions WHERE defType='UpValue')`

### Lambdas
- **clearDefinitions**
    
  *Formula:* `Definition(symbolId=this.id) => no longer valid => definitionCount=0`

### Constraints
- **symbolNameNotEmpty**  
  *Formula:* `symbolName != ''`  
  *Error Message:* A symbol must have a name.
- **uniqueSymbolNameWithinContext**  
  *Formula:* `UNIQUE(symbolName, contextId)`  
  *Error Message:* Symbol name must be unique within the same context.

---

## Entity: Definition

**Description**: Represents a single Wolfram Language definition for a symbol (e.g. a DownValue, UpValue, SubValue, etc.). Contains the pattern/lhs and rhs representations.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **symbolId**  
  *Type:* lookup, *Datatype:*   
  
- **lhsRepresentation**  
  *Type:* scalar, *Datatype:* string  
  
- **rhsRepresentation**  
  *Type:* scalar, *Datatype:* string  
  
- **defType**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **usedSymbolsCount**  
  *Description:* How many other Symbols appear in the rhsRepresentation or condition. Implementation conceptual if references are extracted from parse data.  
  *Formula:* `COUNT(SymbolReference WHERE SymbolReference.definitionId=this.id)`
- **containsPatternArguments**  
  *Description:* True if the lhsRepresentation includes typical pattern constructs (x_, x__, etc.).  
  *Formula:* `REGEX_MATCH(lhsRepresentation,'_+')`

### Lambdas
- **replaceRHS**
  (Parameters: newRhs)  
  *Formula:* `rhsRepresentation == newRhs`


---

## Entity: Context

**Description**: A Wolfram Language context, such as 'System`', 'Global`', or 'MyPackage`', grouping symbols under a namespace-like structure.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **contextName**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **symbols**  
  *Target Entity:* Symbol, *Type:* one_to_many  
    
  (Join condition: **Symbol.contextId = this.id**)  
  *Description:* All symbols that belong to this context.

### Aggregations
- **symbolCount**  
  *Description:* Number of symbols in this context.  
  *Formula:* `COUNT(symbols)`
- **hasPackage**  
  *Description:* True if there exists a Package record referencing this context. Implementation conceptual if contexts map to packages.  
  *Formula:* `EXISTS(Package WHERE Package.defaultContextId=this.id)`


### Constraints
- **contextNameMustEndWithBacktick**  
  *Formula:* `contextName ENDSWITH '`'`  
  *Error Message:* Context name should end with a backtick.

---

## Entity: Package

**Description**: Represents a Wolfram Language package (e.g. .wl or .m file). Contains metadata about exported symbols, associated context, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **packageName**  
  *Type:* scalar, *Datatype:* string  
  
- **defaultContextId**  
  *Type:* lookup, *Datatype:*   
  

### Lookups
- **exportedSymbols**  
  *Target Entity:* Symbol, *Type:* many_to_many  
    
    
  *Description:* All symbols that are officially exported by this package. Implementation conceptual if there's an export table or multiple contexts.

### Aggregations
- **symbolExportCount**  
  *Description:* How many symbols are exported by this package.  
  *Formula:* `COUNT(exportedSymbols)`

### Lambdas
- **exportSymbol**
  (Parameters: symbolId)  
  *Formula:* `Symbol(symbolId).isExportedByPackageId = this.id`


---