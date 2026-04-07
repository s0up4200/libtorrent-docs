---
title: "Stats"
source: "https://libtorrent.org/reference-Stats.html"
---

# counters

Declared in "[libtorrent/performance\_counters.hpp](include/libtorrent/performance_counters.hpp)"

```cpp
struct counters
{
   counters () ;
   counters& operator= (counters const&) & ;
   counters (counters const&) ;
   std::int64_t operator[] (int i) const ;
   std::int64_t inc_stats_counter (int c, std::int64_t value = 1) ;
   void set_value (int c, std::int64_t value) ;
   void blend_stats_counter (int c, std::int64_t value, int ratio) ;
};
```

## operator[]() inc\_stats\_counter()

```cpp
std::int64_t operator[] (int i) const ;
std::int64_t inc_stats_counter (int c, std::int64_t value = 1) ;
```

returns the new value

# stats\_metric

Declared in "[libtorrent/session\_stats.hpp](include/libtorrent/session_stats.hpp)"

describes one statistics metric from the [session](reference-Session.md#session). For more information,
see the [session statistics](manual-ref.md#session-statistics) section.

```cpp
struct stats_metric
{
   char const* name;
   int value_index;
   metric_type_t type;
};
```

name
:   the name of the counter or gauge

value\_index type
:   the index into the [session](reference-Session.md#session) stats array, where the underlying value of
    this counter or gauge is found. The [session](reference-Session.md#session) stats array is part of the
    [session\_stats\_alert](reference-Alerts.md#session_stats_alert) object.

# session\_stats\_metrics()

Declared in "[libtorrent/session\_stats.hpp](include/libtorrent/session_stats.hpp)"

```cpp
std::vector<stats_metric> session_stats_metrics ();
```

This free function returns the list of available metrics exposed by
libtorrent's statistics API. Each metric has a name and a *value index*.
The value index is the index into the array in [session\_stats\_alert](reference-Alerts.md#session_stats_alert) where
this metric's value can be found when the [session](reference-Session.md#session) stats is sampled (by
calling [post\_session\_stats()](reference-Session.md#post_session_stats())).

# find\_metric\_idx()

Declared in "[libtorrent/session\_stats.hpp](include/libtorrent/session_stats.hpp)"

```cpp
int find_metric_idx (string_view name);
```

given a name of a metric, this function returns the counter index of it,
or -1 if it could not be found. The counter index is the index into the
values array returned by [session\_stats\_alert](reference-Alerts.md#session_stats_alert).

# enum metric\_type\_t

Declared in "[libtorrent/session\_stats.hpp](include/libtorrent/session_stats.hpp)"

| name | value | description |
| --- | --- | --- |
| counter | 0 |  |
| gauge | 1 |  |
