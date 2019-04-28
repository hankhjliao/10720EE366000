# Schedule

## Timetable

|      Week      |       Date        | Goal          | Note           |
| :------------: | :---------------: | :------------ | :------------- |
| [11](./worklog.md#week-11) | 2019-05-01 (Wed.) | Confirm Proj. |
| [12](./worklog.md#week-12) | 2019-05-08 (Wed.) |               |
| [13](./worklog.md#week-13) | 2019-05-15 (Wed.) |               |
| [14](./worklog.md#week-14) | 2019-05-22 (Wed.) |               | Proj. Proposal |
| [15](./worklog.md#week-15) | 2019-05-29 (Wed.) |               |
| [16](./worklog.md#week-16) | 2019-06-05 (Wed.) | Finish Proj.  |
| [17](./worklog.md#week-17) | 2019-06-12 (Wed.) | Proj. Hotfix  |
| [18](./worklog.md#week-18) | 2019-06-19 (Wed.) |               | Proj. Demo     |

## Gantt Graph

```mermaid
gantt
    title Proj. Schedule
    dateFormat  YYYY-MM-DD

    section Prepare
    Confirm Proj.        :p10, 2019-05-01, 3d
    Write Proj. Proposal :p20, after p10, 3d

    section Research
    Algoritm             :r10, after p10, 21d
    Algoritm (Backup)    :r20, 2019-05-13, 21d

    section Implement
    Program Backend      :i10, 2019-05-15, 21d
    Program GUI          :i20, 2019-05-22, 21d

    section Bonus
    Document             :b10, after r10, 20d
    Website              :b20, after i10, 2019-06-18
```
