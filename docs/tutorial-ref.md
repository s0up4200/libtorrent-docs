---
title: "tutorial"
source: "https://libtorrent.org/tutorial-ref.html"
---

# tutorial

The fundamental feature of starting and downloading torrents in libtorrent is
achieved by creating a *session*, which provides the context and a container for
torrents. This is done with via the [session](reference-Session.md#session) class, most of its interface is
documented under [session\_handle](reference-Session.md#session_handle) though.

To add a torrent to the [session](reference-Session.md#session), you fill in an [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object and
pass it either to [add\_torrent()](reference-Session.md#add_torrent()) or [async\_add\_torrent()](reference-Session.md#async_add_torrent()).

add\_torrent() is a blocking call which returns a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle).

For example:

```cpp
#include <libtorrent/session.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/torrent_handle.hpp>
#include <libtorrent/magnet_uri.hpp>

int main(int argc, char const* argv[])
{
        if (argc != 2) {
                fprintf(stderr, "usage: %s <magnet-url>\n");
                return 1;
        }
        lt::session ses;

        lt::add_torrent_params atp = lt::parse_magnet_uri(argv[1]);
        atp.save_path = "."; // save in current dir
        lt::torrent_handle h = ses.add_torrent(atp);

        // ...
}
```

Once you have a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle), you can affect it as well as querying status.
First, let's extend the example to print out messages from the bittorrent engine
about progress and events happening under the hood. libtorrent has a mechanism
referred to as *alerts* to communicate back information to the client application.

Clients can poll a [session](reference-Session.md#session) for new alerts via the [pop\_alerts()](reference-Session.md#pop_alerts()) call. This
function fills in a vector of [alert](reference-Alerts.md#alert) pointers with all new alerts since the last
call to this function. The pointers are owned by the [session](reference-Session.md#session) object at will
become invalidated by the next call to [pop\_alerts()](reference-Session.md#pop_alerts()).

The alerts form a class hierarchy with [alert](reference-Alerts.md#alert) as the root class. Each specific
kind of [alert](reference-Alerts.md#alert) may include additional state, specific to the kind of message. All
alerts implement a [message()](reference-Alerts.md#message()) function that prints out pertinent information
of the [alert](reference-Alerts.md#alert) message. This can be convenient for simply logging events.

For programmatically react to certain events, use alert\_cast to attempt
a down cast of an [alert](reference-Alerts.md#alert) object to a more specific type.

In order to print out events from libtorrent as well as exiting when the torrent
completes downloading, we can poll the [session](reference-Session.md#session) for alerts periodically and print
them out, as well as listening for the [torrent\_finished\_alert](reference-Alerts.md#torrent_finished_alert), which is posted
when a torrent completes.

```cpp
#include <iostream>
#include <thread>
#include <chrono>

#include <libtorrent/session.hpp>
#include <libtorrent/session_params.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/torrent_handle.hpp>
#include <libtorrent/alert_types.hpp>
#include <libtorrent/magnet_uri.hpp>

int main(int argc, char const* argv[]) try
{
  if (argc != 2) {
    std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
    return 1;
  }
  lt::settings_pack p;
  p.set_int(lt::settings_pack::alert_mask, lt::alert_category::status
    | lt::alert_category::error);
  lt::session ses(p);

  lt::add_torrent_params atp = lt::parse_magnet_uri(argv[1]);
  atp.save_path = "."; // save in current dir
  lt::torrent_handle h = ses.add_torrent(std::move(atp));

  for (;;) {
    std::vector<lt::alert*> alerts;
    ses.pop_alerts(&alerts);

    for (lt::alert const* a : alerts) {
      std::cout << a->message() << std::endl;
      // if we receive the finished alert or an error, we're done
      if (lt::alert_cast<lt::torrent_finished_alert>(a)) {
        goto done;
      }
      if (lt::alert_cast<lt::torrent_error_alert>(a)) {
        goto done;
      }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
  }
  done:
  std::cout << "done, shutting down" << std::endl;
}
catch (std::exception& e)
{
  std::cerr << "Error: " << e.what() << std::endl;
}
```

## alert masks

The output from this program will be quite verbose, which is probably a good
starting point to get some understanding of what's going on. Alerts are
categorized into [alert](reference-Alerts.md#alert) categories. Each category can be enabled and disabled
independently via the *alert mask*.

The [alert](reference-Alerts.md#alert) mask is a configuration option offered by libtorrent. There are many
configuration options, see [settings\_pack](reference-Settings.md#settings_pack). The alert\_mask setting is an integer
of the category flags ORed together.

For instance, to only see the most pertinent alerts, the [session](reference-Session.md#session) can be
constructed like this:

```cpp
lt::settings_pack pack;
pack.set_int(lt::settings_pack::alert_mask
        , lt::alert_category::error
        | lt::alert_category::storage
        | lt::alert_category::status);

lt::session ses(pack);
```

Configuration options can be updated after the [session](reference-Session.md#session) is started by calling
[apply\_settings()](reference-Session.md#apply_settings()). Some settings are best set before starting the [session](reference-Session.md#session)
though, like listen\_interfaces, to avoid race conditions. If you start the
[session](reference-Session.md#session) with the default settings and then immediately change them, there will
still be a window where the default settings apply.

Changing the settings may trigger listen sockets to close and re-open and
NAT-PMP, UPnP updates to be sent. For this reason, it's typically a good idea
to batch settings updates into a single call.

## session destruction

The [session](reference-Session.md#session) destructor is blocking by default. When shutting down, trackers
will need to be contacted to stop torrents and other outstanding operations
need to be cancelled. Shutting down can sometimes take several seconds,
primarily because of trackers that are unresponsive (and time out) and also
DNS servers that are unresponsive. DNS lookups are especially difficult to
abort when stalled.

In order to be able to start destruction asynchronously, one can call
[session::abort()](reference-Session.md#abort()).

This call returns a [session\_proxy](reference-Session.md#session_proxy) object, which is a handle keeping the [session](reference-Session.md#session)
state alive while shutting it down. It deliberately does not provide any of the
[session](reference-Session.md#session) operations, since it's shutting down.

After having a [session\_proxy](reference-Session.md#session_proxy) object, the [session](reference-Session.md#session) destructor does not block.
However, the [session\_proxy](reference-Session.md#session_proxy) destructor *will*.

This can be used to shut down multiple sessions or other parts of the
application in parallel.

## asynchronous operations

Essentially any call to a member function of [session](reference-Session.md#session) or [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) that
returns a value is a blocking synchronous call. Meaning it will post a message
to the main libtorrent thread and wait for a response. Such calls may be
expensive, and in applications where stalls should be avoided (such as user
interface threads), blocking calls should be avoided.

In the example above, session::add\_torrent() returns a [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) and is
thus blocking. For higher efficiency, [async\_add\_torrent()](reference-Session.md#async_add_torrent()) will post a message
to the main thread to add a torrent, and post the resulting [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) back
in an [alert](reference-Alerts.md#alert) ([add\_torrent\_alert](reference-Alerts.md#add_torrent_alert)). This is especially useful when adding a lot
of torrents in quick succession, as there's no stall in between calls.

In the example above, we don't actually use the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) for anything, so
converting it to use [async\_add\_torrent()](reference-Session.md#async_add_torrent()) is just a matter of replacing the
[add\_torrent()](reference-Session.md#add_torrent()) call with [async\_add\_torrent()](reference-Session.md#async_add_torrent()).

## torrent\_status\_updates

To get updates to the status of torrents, call [post\_torrent\_updates()](reference-Session.md#post_torrent_updates()) on the
[session](reference-Session.md#session) object. This will cause libtorrent to post a [state\_update\_alert](reference-Alerts.md#state_update_alert)
containing [torrent\_status](reference-Torrent_Status.md#torrent_status) objects for all torrents whose status has *changed*
since the last call to [post\_torrent\_updates()](reference-Session.md#post_torrent_updates()).

The [state\_update\_alert](reference-Alerts.md#state_update_alert) looks something like this:

```cpp
struct state_update_alert : alert
{
        virtual std::string message() const;
        std::vector<torrent_status> status;
};
```

The status field only contains the [torrent\_status](reference-Torrent_Status.md#torrent_status) for torrents with
updates since the last call. It may be empty if no torrent has updated its
state. This feature is critical for scalability.

See the [torrent\_status](reference-Torrent_Status.md#torrent_status) object for more information on what is in there.
Perhaps the most interesting fields are total\_payload\_download,
total\_payload\_upload, num\_peers and state.

## resuming torrents

Since bittorrent downloads pieces of files in random order, it's not trivial to
resume a partial download. When resuming a download, the bittorrent engine must
restore the state of the downloading torrent, specifically which parts of the
file(s) are downloaded. There are two approaches to doing this:

1. read every piece of the downloaded files from disk and compare it against its
   expected hash.
2. save, to disk, the state of which pieces (and partial pieces) are downloaded,
   and load it back in again when resuming.

If no resume data is provided with a torrent that's added, libtorrent will
employ (1) by default.

To save resume data, call [save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()) on the [torrent\_handle](reference-Torrent_Handle.md#torrent_handle) object.
This will ask libtorrent to generate the resume data and post it back in
a [save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert). If generating the resume data fails for any reason,
a [save\_resume\_data\_failed\_alert](reference-Alerts.md#save_resume_data_failed_alert) is posted instead.

Exactly one of those alerts will be posted for every call to
[save\_resume\_data()](reference-Torrent_Handle.md#save_resume_data()). This is an important property when shutting down a
[session](reference-Session.md#session) with multiple torrents, every resume [alert](reference-Alerts.md#alert) must be handled before
resuming with shut down. Any torrent may fail to save resume data, so the client
would need to keep a count of the outstanding resume files, decremented on
either [save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert) or [save\_resume\_data\_failed\_alert](reference-Alerts.md#save_resume_data_failed_alert).

The [save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert) looks something like this:

```cpp
struct save_resume_data_alert : torrent_alert
{
        virtual std::string message() const;

        // the resume data
        add_torrent_params params;
};
```

The params field is an [add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params) object containing all the state
to add the torrent back to the [session](reference-Session.md#session) again. This object can be serialized
using [write\_resume\_data()](reference-Resume_Data.md#write_resume_data()) or [write\_resume\_data\_buf()](reference-Resume_Data.md#write_resume_data_buf()), and de-serialized
with [read\_resume\_data()](reference-Resume_Data.md#read_resume_data()).

## example

Here's an updated version of the above example with the following updates:

1. not using blocking calls
2. printing torrent status updates rather than the raw log
3. saving and loading resume files

```cpp
#include <iostream>
#include <thread>
#include <chrono>
#include <fstream>

#include <libtorrent/session.hpp>
#include <libtorrent/session_params.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/torrent_handle.hpp>
#include <libtorrent/alert_types.hpp>
#include <libtorrent/bencode.hpp>
#include <libtorrent/torrent_status.hpp>
#include <libtorrent/read_resume_data.hpp>
#include <libtorrent/write_resume_data.hpp>
#include <libtorrent/error_code.hpp>
#include <libtorrent/magnet_uri.hpp>

namespace {

using clk = std::chrono::steady_clock;

// return the name of a torrent status enum
char const* state(lt::torrent_status::state_t s)
{
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wcovered-switch-default"
#endif
  switch(s) {
    case lt::torrent_status::checking_files: return "checking";
    case lt::torrent_status::downloading_metadata: return "dl metadata";
    case lt::torrent_status::downloading: return "downloading";
    case lt::torrent_status::finished: return "finished";
    case lt::torrent_status::seeding: return "seeding";
    case lt::torrent_status::checking_resume_data: return "checking resume";
    default: return "<>";
  }
#ifdef __clang__
#pragma clang diagnostic pop
#endif
}

} // anonymous namespace

int main(int argc, char const* argv[]) try
{
  if (argc != 2) {
    std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
    return 1;
  }

  lt::settings_pack pack;
  pack.set_int(lt::settings_pack::alert_mask
    , lt::alert_category::error
    | lt::alert_category::storage
    | lt::alert_category::status);

  lt::session ses(pack);
  clk::time_point last_save_resume = clk::now();

  // load resume data from disk and pass it in as we add the magnet link
  std::ifstream ifs(".resume_file", std::ios_base::binary);
  ifs.unsetf(std::ios_base::skipws);
  std::vector<char> buf{std::istream_iterator<char>(ifs)
    , std::istream_iterator<char>()};

  lt::add_torrent_params magnet = lt::parse_magnet_uri(argv[1]);
  if (buf.size()) {
    lt::add_torrent_params atp = lt::read_resume_data(buf);
    if (atp.info_hashes == magnet.info_hashes) magnet = std::move(atp);
  }
  magnet.save_path = "."; // save in current dir
  ses.async_add_torrent(std::move(magnet));

  // this is the handle we'll set once we get the notification of it being
  // added
  lt::torrent_handle h;

  // set when we're exiting
  bool done = false;
  for (;;) {
    std::vector<lt::alert*> alerts;
    ses.pop_alerts(&alerts);

    for (lt::alert const* a : alerts) {
      if (auto at = lt::alert_cast<lt::add_torrent_alert>(a)) {
        h = at->handle;
      }
      // if we receive the finished alert or an error, we're done
      if (lt::alert_cast<lt::torrent_finished_alert>(a)) {
        h.save_resume_data(lt::torrent_handle::only_if_modified
          | lt::torrent_handle::save_info_dict);
        done = true;
      }
      if (lt::alert_cast<lt::torrent_error_alert>(a)) {
        std::cout << a->message() << std::endl;
        done = true;
        h.save_resume_data(lt::torrent_handle::only_if_modified
          | lt::torrent_handle::save_info_dict);
      }

      // when resume data is ready, save it
      if (auto rd = lt::alert_cast<lt::save_resume_data_alert>(a)) {
        std::ofstream of(".resume_file", std::ios_base::binary);
        of.unsetf(std::ios_base::skipws);
        auto const b = write_resume_data_buf(rd->params);
        of.write(b.data(), int(b.size()));
        if (done) goto done;
      }

      if (lt::alert_cast<lt::save_resume_data_failed_alert>(a)) {
        if (done) goto done;
      }

      if (auto st = lt::alert_cast<lt::state_update_alert>(a)) {
        if (st->status.empty()) continue;

        // we only have a single torrent, so we know which one
        // the status is for
        lt::torrent_status const& s = st->status[0];
        std::cout << '\r' << state(s.state) << ' '
          << (s.download_payload_rate / 1000) << " kB/s "
          << (s.total_done / 1000) << " kB ("
          << (s.progress_ppm / 10000) << "%) downloaded ("
          << s.num_peers << " peers)\x1b[K";
        std::cout.flush();
      }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    // ask the session to post a state_update_alert, to update our
    // state output for the torrent
    ses.post_torrent_updates();

    // save resume data once every 30 seconds
    if (clk::now() - last_save_resume > std::chrono::seconds(30)) {
      h.save_resume_data(lt::torrent_handle::only_if_modified
        | lt::torrent_handle::save_info_dict);
      last_save_resume = clk::now();
    }
  }

done:
  std::cout << "\ndone, shutting down" << std::endl;
}
catch (std::exception& e)
{
  std::cerr << "Error: " << e.what() << std::endl;
}
```

## session state

On construction, a [session](reference-Session.md#session) object is configured by a [session\_params](reference-Session.md#session_params) object. The
[session\_params](reference-Session.md#session_params) object notably contain session\_settings, the state of the DHT
node (e.g. routing table), the session's IP filter as well as the disk I/O
back-end and dht storage to use.

There are functions to serialize and de-serialize the [session\_params](reference-Session.md#session_params) object to
help in restoring [session](reference-Session.md#session) state from last run. Doing so is especially helpful
for bootstrapping the DHT, using nodes from last run.

Before destructing the [session](reference-Session.md#session) object, call session::session\_state() to get
the current state as a [session\_params](reference-Session.md#session_params) object.

Call [write\_session\_params()](reference-Session.md#write_session_params()) or [write\_session\_params\_buf()](reference-Session.md#write_session_params_buf()) to serialize the state
into a bencoded [entry](reference-Bencoding.md#entry) or to a flat buffer (std::vector<char>) respectively.

On startup, before constructing the [session](reference-Session.md#session) object, load the buffer back from
disk and call [read\_session\_params()](reference-Session.md#read_session_params()) to de-serialize it back into a [session\_params](reference-Session.md#session_params)
object. Before passing it into the [session](reference-Session.md#session) constructor is your chance to set
update the [settings\_pack](reference-Settings.md#settings_pack) (params) member of settings\_params, or configuring
the disk\_io\_constructor.

## example

Another updated version of the above example with the following updates:

1. load and save [session\_params](reference-Session.md#session_params) to file ".session"
2. allow shutting down on SIGINT

```cpp
#include <iostream>
#include <thread>
#include <chrono>
#include <fstream>
#include <csignal>

#include <libtorrent/session.hpp>
#include <libtorrent/session_params.hpp>
#include <libtorrent/add_torrent_params.hpp>
#include <libtorrent/torrent_handle.hpp>
#include <libtorrent/alert_types.hpp>
#include <libtorrent/bencode.hpp>
#include <libtorrent/torrent_status.hpp>
#include <libtorrent/read_resume_data.hpp>
#include <libtorrent/write_resume_data.hpp>
#include <libtorrent/error_code.hpp>
#include <libtorrent/magnet_uri.hpp>

namespace {

using clk = std::chrono::steady_clock;

// return the name of a torrent status enum
char const* state(lt::torrent_status::state_t s)
{
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wcovered-switch-default"
#endif
  switch(s) {
    case lt::torrent_status::checking_files: return "checking";
    case lt::torrent_status::downloading_metadata: return "dl metadata";
    case lt::torrent_status::downloading: return "downloading";
    case lt::torrent_status::finished: return "finished";
    case lt::torrent_status::seeding: return "seeding";
    case lt::torrent_status::checking_resume_data: return "checking resume";
    default: return "<>";
  }
#ifdef __clang__
#pragma clang diagnostic pop
#endif
}

std::vector<char> load_file(char const* filename)
{
  std::ifstream ifs(filename, std::ios_base::binary);
  ifs.unsetf(std::ios_base::skipws);
  return {std::istream_iterator<char>(ifs), std::istream_iterator<char>()};
}

// set when we're exiting
std::atomic<bool> shut_down{false};

void sighandler(int) { shut_down = true; }

} // anonymous namespace

int main(int argc, char const* argv[]) try
{
  if (argc != 2) {
    std::cerr << "usage: " << argv[0] << " <magnet-url>" << std::endl;
    return 1;
  }

  // load session parameters
  auto session_params = load_file(".session");
  lt::session_params params = session_params.empty()
    ? lt::session_params() : lt::read_session_params(session_params);
  params.settings.set_int(lt::settings_pack::alert_mask
    , lt::alert_category::error
    | lt::alert_category::storage
    | lt::alert_category::status);

  lt::session ses(params);
  clk::time_point last_save_resume = clk::now();

  // load resume data from disk and pass it in as we add the magnet link
  auto buf = load_file(".resume_file");

  lt::add_torrent_params magnet = lt::parse_magnet_uri(argv[1]);
  if (buf.size()) {
    lt::add_torrent_params atp = lt::read_resume_data(buf);
    if (atp.info_hashes == magnet.info_hashes) magnet = std::move(atp);
  }
  magnet.save_path = "."; // save in current dir
  ses.async_add_torrent(std::move(magnet));

  // this is the handle we'll set once we get the notification of it being
  // added
  lt::torrent_handle h;

  std::signal(SIGINT, &sighandler);

  // set when we're exiting
  bool done = false;
  for (;;) {
    std::vector<lt::alert*> alerts;
    ses.pop_alerts(&alerts);

    if (shut_down) {
      shut_down = false;
      auto const handles = ses.get_torrents();
      if (handles.size() == 1) {
        handles[0].save_resume_data(lt::torrent_handle::only_if_modified
          | lt::torrent_handle::save_info_dict);
        done = true;
      }
    }

    for (lt::alert const* a : alerts) {
      if (auto at = lt::alert_cast<lt::add_torrent_alert>(a)) {
        h = at->handle;
      }
      // if we receive the finished alert or an error, we're done
      if (lt::alert_cast<lt::torrent_finished_alert>(a)) {
        h.save_resume_data(lt::torrent_handle::only_if_modified
          | lt::torrent_handle::save_info_dict);
        done = true;
      }
      if (lt::alert_cast<lt::torrent_error_alert>(a)) {
        std::cout << a->message() << std::endl;
        done = true;
        h.save_resume_data(lt::torrent_handle::only_if_modified
          | lt::torrent_handle::save_info_dict);
      }

      // when resume data is ready, save it
      if (auto rd = lt::alert_cast<lt::save_resume_data_alert>(a)) {
        std::ofstream of(".resume_file", std::ios_base::binary);
        of.unsetf(std::ios_base::skipws);
        auto const b = write_resume_data_buf(rd->params);
        of.write(b.data(), int(b.size()));
        if (done) goto done;
      }

      if (lt::alert_cast<lt::save_resume_data_failed_alert>(a)) {
        if (done) goto done;
      }

      if (auto st = lt::alert_cast<lt::state_update_alert>(a)) {
        if (st->status.empty()) continue;

        // we only have a single torrent, so we know which one
        // the status is for
        lt::torrent_status const& s = st->status[0];
        std::cout << '\r' << state(s.state) << ' '
          << (s.download_payload_rate / 1000) << " kB/s "
          << (s.total_done / 1000) << " kB ("
          << (s.progress_ppm / 10000) << "%) downloaded ("
          << s.num_peers << " peers)\x1b[K";
        std::cout.flush();
      }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    // ask the session to post a state_update_alert, to update our
    // state output for the torrent
    ses.post_torrent_updates();

    // save resume data once every 30 seconds
    if (clk::now() - last_save_resume > std::chrono::seconds(30)) {
      h.save_resume_data(lt::torrent_handle::only_if_modified
        | lt::torrent_handle::save_info_dict);
      last_save_resume = clk::now();
    }
  }

done:
  std::cout << "\nsaving session state" << std::endl;
  {
    std::ofstream of(".session", std::ios_base::binary);
    of.unsetf(std::ios_base::skipws);
    auto const b = write_session_params_buf(ses.session_state()
      , lt::save_state_flags_t::all());
    of.write(b.data(), int(b.size()));
  }

  std::cout << "\ndone, shutting down" << std::endl;
}
catch (std::exception& e)
{
  std::cerr << "Error: " << e.what() << std::endl;
}
```

## torrent files

To add torrent files to a [session](reference-Session.md#session) (as opposed to a magnet link), it must first
be loaded into a [torrent\_info](reference-Torrent_Info.md#torrent_info) object.

The [torrent\_info](reference-Torrent_Info.md#torrent_info) object can be created either by filename a buffer or a
bencoded structure. When adding by filename, there's a sanity check limit on the
size of the file, for adding arbitrarily large torrents, load the file outside
of the constructor.

The [torrent\_info](reference-Torrent_Info.md#torrent_info) object provides an opportunity to query information about the
.torrent file as well as mutating it before adding it to the [session](reference-Session.md#session).

## bencoding

bencoded structures is the default data storage format used by bittorrent, such
as .torrent files, tracker announce and scrape responses and some wire protocol
extensions. libtorrent provides an efficient framework for decoding bencoded
data through [bdecode()](reference-Bdecoding.md#bdecode()) function.

There are two separate mechanisms for *encoding* and *decoding*. When decoding,
use the [bdecode()](reference-Bdecoding.md#bdecode()) function that returns a [bdecode\_node](reference-Bdecoding.md#bdecode_node). When encoding, use
[bencode()](reference-Bencoding.md#bencode()) taking an [entry](reference-Bencoding.md#entry) object.

The key property of [bdecode()](reference-Bdecoding.md#bdecode()) is that it does not copy any data out of the
buffer that was parsed. It builds the tree structures of references pointing
into the buffer. The buffer must stay alive and valid for as long as the
[bdecode\_node](reference-Bdecoding.md#bdecode_node) is in use.

For performance details on [bdecode()](reference-Bdecoding.md#bdecode()), see the [blog post](https://blog.libtorrent.org/2015/03/bdecode-parsers/) about it.
