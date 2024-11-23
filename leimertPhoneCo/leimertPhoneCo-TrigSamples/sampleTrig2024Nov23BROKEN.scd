// s.options.memSize = 32768;

s.waitForBoot({
	var arrayOfBuffers;

	arrayOfBuffers = "/home/sound/LeimertPhoneCo/NoPriorArt/*".pathMatch.collect {|file| Buffer.read(s,
file);};

	s.sync;

	SynthDef( \play, { | amp, buf, rate = 1.0, trig = 0 |
		var env, sig;
		env = EnvGen.kr(Env.linen(0.001, BufDur.kr(buf), 0.001), trig, doneAction: Done.freeSelf);
		sig = PlayBuf.ar(1, buf, rate, trig);
		Out.ar(0, sig * env);
	}).add;

	OSCFunc( { |msg|
		var sampleNum;
		// msg.postln;
		sampleNum = msg[1];
		( "Now Playing" + sampleNum ).postln;
		Synth.new( \play, [ \amp, 0.85, \buf, arrayOfBuffers[sampleNum], \trig, 1 ] );
	}, "/engine" );
});
