package gps;

import gps.api.GpsState;

public class GpsNode {

  private GpsState state;

  private GpsNode parent;

  private Integer cost;

  public GpsNode(GpsState state, Integer cost) {
    this.state = state;
    this.cost = cost;
  }

  public GpsNode getParent() {
    return parent;
  }

  public void setParent(GpsNode parent) {
    this.parent = parent;
  }

  public GpsState getState() {
    return state;
  }

  public Integer getCost() {
    return cost;
  }

  @Override
  public String toString() {
    return state.toString();
  }

  /**
   * TODO
   * @return solution as string.
   */
  public String getSolution() {
    if (this.parent == null) {
      return this.state.toString();
    }
    return this.parent.getSolution() + this.state.toString();
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    GpsNode other = (GpsNode) obj;
    if (state == null) {
      if (other.state != null) {
        return false;
      }
    } else if (!state.equals(other.state)) {
      return false;
    }
    return true;
  }

  @Override
  public int hashCode() {
    int result = state.hashCode();
    result = 31 * result + parent.hashCode();
    result = 31 * result + cost.hashCode();
    return result;
  }
}
