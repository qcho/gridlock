package ar.edu.itba.sia.c12017.g5.gridlock.utilities;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.FileReader;
import java.nio.file.Path;

/**
 * Created by alebian on 14/03/17.
 */
public class BoardParser {
  private Path path;

  public BoardParser(Path path) {
    this.path = path.toAbsolutePath();
  }

  /*
  * The expected format:
  * {
  *   "board": {
  *       "size": {
  *           "rows": Integer,
  *           "columns": Integer
  *       },
  *       "exit": {
  *           "position": {
  *               "x": Integer,
  *               "y": Integer
  *           }
  *       },
  *       "chips":[
  *           {
  *               "main": Boolean,
  *               "start_position": {
  *                   "x": Integer,
  *                   "y": Integer
  *               },
  *               "end_position": {
  *                   "x": Integer,
  *                   "y": Integer
  *               }
  *           },
  *           ...
  *       ]
  *   }
  * }
  * */
  public Board parse() {
    JSONParser parser = new JSONParser();
    Board answer = null;
    try {
      Object obj = parser.parse(new FileReader(path.toString()));
      JSONObject json = (JSONObject) obj;
      JSONObject boardInfo = (JSONObject) json.get("board");
      JSONObject size = (JSONObject) boardInfo.get("size");
      JSONObject exit = (JSONObject) ((JSONObject) boardInfo.get("exit")).get("position");
      JSONArray chips = (JSONArray) boardInfo.get("chips");
      Board board = new Board((long) size.get("rows"), (long) size.get("columns"), (long) exit.get("x"), (long) exit.get("y"));
      chips.forEach(c -> {
        boolean main = (boolean) ((JSONObject) c).get("main");
        JSONObject start = (JSONObject) ((JSONObject) c).get("start_position");
        JSONObject end = (JSONObject) ((JSONObject) c).get("end_position");
        board.addChip(main, (long) start.get("x"), (long) start.get("y"), (long) end.get("x"), (long) end.get("y"));
      });
      answer = board;
    } catch (Exception e) {
      System.out.println(e.getMessage());
    }
    return answer;
  }
}
