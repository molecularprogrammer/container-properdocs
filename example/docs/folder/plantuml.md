---
tags:
  - plantuml
  - ditaa
---

# PlantUML Example

## Dependency Diagram

```plantuml

package component1 {
  node subcomponent1_1
  node subcomponent1_2
}

package component2 {
  node subcomponent2_1
}

subcomponent2_1 ->subcomponent1_1
subcomponent2_1 ->subcomponent1_2
```

### Activity Diagram

```plantuml
start
repeat
  :read data;
  :generate diagrams;
repeat while (more data?) is (yes)
->no;
stop
```

### DITAA Digram

```ditaa{kroki=true}
+--------+
|  Start |
+--+-----+
   |
   v
+------------+
| Processing |
+--+---------+
   |
   v
+--+-----+
|  End   |
+--------+   
```

