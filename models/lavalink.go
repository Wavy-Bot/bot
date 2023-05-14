package models

import (
	"github.com/disgoorg/disgolink/v2/disgolink"
	"github.com/disgoorg/disgolink/v2/lavalink"
	"github.com/disgoorg/snowflake/v2"
	"math/rand"
)

// LavalinkQueueType is the type of the Lavalink queue.
type LavalinkQueueType string

const (
	// LavalinkQueueTypeNormal is the normal queue type.
	LavalinkQueueTypeNormal LavalinkQueueType = "normal"
	// LavalinkQueueTypeRepeatTrack is the repeat track queue type.
	LavalinkQueueTypeRepeatTrack LavalinkQueueType = "repeat_track"
	// LavalinkQueueTypeRepeatQueue is the repeat queue queue type.
	LavalinkQueueTypeRepeatQueue LavalinkQueueType = "repeat_queue"
)

// String returns the string representation of the LavalinkQueueType.
func (q LavalinkQueueType) String() string {
	switch q {
	case LavalinkQueueTypeNormal:
		return "Normal"
	case LavalinkQueueTypeRepeatTrack:
		return "Repeat Track"
	case LavalinkQueueTypeRepeatQueue:
		return "Repeat LavalinkQueue"
	default:
		return "unknown"
	}
}

// Lavalink contains the Lavalink client and the queues.
type Lavalink struct {
	// Client is the Lavalink client.
	Client disgolink.Client
	// Queues is the Lavalink queues.
	Queues *LavalinkQueueManager
}

// LavalinkNodes contains the Lavalink nodes.
type LavalinkNodes struct {
	Nodes []disgolink.NodeConfig `json:"nodes"`
}

// LavalinkQueue contains the Lavalink queue.
type LavalinkQueue struct {
	// Tracks is the tracks in the queue.
	Tracks []lavalink.Track
	// Type is the type of the queue.
	Type LavalinkQueueType
}

// Shuffle shuffles the tracks in the queue.
func (q *LavalinkQueue) Shuffle() {
	rand.Shuffle(len(q.Tracks), func(i, j int) {
		q.Tracks[i], q.Tracks[j] = q.Tracks[j], q.Tracks[i]
	})
}

// Add adds tracks to the queue.
func (q *LavalinkQueue) Add(track ...lavalink.Track) {
	q.Tracks = append(q.Tracks, track...)
}

// Next returns the next track in the queue.
func (q *LavalinkQueue) Next() (lavalink.Track, bool) {
	if len(q.Tracks) == 0 {
		return lavalink.Track{}, false
	}
	track := q.Tracks[0]
	q.Tracks = q.Tracks[1:]
	return track, true
}

// Skip skips the specified amount of tracks in the queue.
func (q *LavalinkQueue) Skip(amount int) (lavalink.Track, bool) {
	if len(q.Tracks) == 0 {
		return lavalink.Track{}, false
	}
	if amount > len(q.Tracks) {
		amount = len(q.Tracks)
	}
	q.Tracks = q.Tracks[amount:]
	return q.Tracks[0], true
}

// Clear clears the queue.
func (q *LavalinkQueue) Clear() {
	q.Tracks = make([]lavalink.Track, 0)
}

// LavalinkQueueManager contains the Lavalink queues.
type LavalinkQueueManager struct {
	Queues map[snowflake.ID]*LavalinkQueue
}

// Get returns the Lavalink queue for the specified guild.
func (q *LavalinkQueueManager) Get(guildID snowflake.ID) *LavalinkQueue {
	queue, ok := q.Queues[guildID]
	if !ok {
		queue = &LavalinkQueue{
			Tracks: make([]lavalink.Track, 0),
			Type:   LavalinkQueueTypeNormal,
		}
		q.Queues[guildID] = queue
	}
	return queue
}

// Delete deletes the Lavalink queue for the specified guild.
func (q *LavalinkQueueManager) Delete(guildID snowflake.ID) {
	delete(q.Queues, guildID)
}
