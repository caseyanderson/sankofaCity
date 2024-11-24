s.options.memSize = 32768;

s.waitForBoot({
	var arrayOfBuffers;

	arrayOfBuffers = "/home/sound/leimertPhoneCo-AudioFiles/NoPriorArt/*".pathMatch.collect {|file| Buffer.read(s,
file);};

	s.sync;

	// block multiple file playback
	n = NetAddr("127.0.0.1", 58110);

	SynthDef( \play, { | amp, buf, rate = 1.0, trig = 0 |
		var env, sig;
		sig = PlayBuf.ar(1, buf, rate, trig, doneAction: Done.freeSelf);
		Out.ar(0, sig);
	}).add;

	OSCdef(\phonePlayBack, { |msg|
		var sampleNum;
		// msg.postln;
		sampleNum = msg[1];
		( "Now Playing" + sampleNum ).postln;
		Synth.new( \play, [ \amp, 0.85, \buf, arrayOfBuffers[sampleNum], \trig, 1 ] ).onFree{
			"done!".postln;
			n.sendMsg("/nowPlaying", "FALSE");
		};
	}, "/engine" );
});

