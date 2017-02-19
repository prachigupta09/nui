using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Speech.Recognition;
using System.Speech.Recognition.SrgsGrammar;
using System.IO;
using System.Xml;


namespace Test
{
    class Program
    { 
        static void Main(string[] args)
        {
            SpeechRecognitionEngine recognizer = new SpeechRecognitionEngine();
            string filepath = @"D:\Documents\Visual Studio 2015\Projects\Test\Test\chess.xml";
            Grammar AN = new Grammar(filepath);
            recognizer.LoadGrammar(AN);
            // I assume multiple grammars can be loaded.

            while (true)
            {
                try
                {
                    Console.WriteLine("Speak now!");
                    recognizer.SetInputToDefaultAudioDevice();
                    RecognitionResult result = recognizer.Recognize();
                    Console.WriteLine(result.Text);
                }
                catch (InvalidOperationException exception)
                {
                    Console.WriteLine(String.Format("Could not recognize input from default aduio device. Is a microphone or sound card available?\r\n{0} - {1}.", exception.Source, exception.Message));
                }
            }


            recognizer.UnloadAllGrammars();




        }
    }
}
